import sys
import rtmidi
import threading
import time
import board
import neopixel
import math
import random

dev = rtmidi.RtMidiIn()
collectors = []
pixel_pin = board.D18
num_pixels = 150
brightness = 0.7
wait = 0.003
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)
from_wait = 0.2
to_wait = 0.001
max_ti = 10

def rescale(value,min,max,omin,omax):
    print(value,min,max,omin,omax)
    value = (omax - omin) * (value - min)/(max- min) + omin
    if value < omin:
      value = omin
    if value > omax:
      value = omax
    return(int(value))

def print_message(midi, port):
    if midi.isNoteOn():
        print('%s: ON: ' % port, midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
    elif midi.isNoteOff():
        print('%s: OFF:' % port, midi.getMidiNoteName(midi.getNoteNumber()))
    elif midi.isController():
        print('%s: CONTROLLER' % port, midi.getControllerNumber(), midi.getControllerValue())
   
    print(midi)

class NoEffect(threading.Thread):
    def __init__(self):
        pass

    def beat(self):
        # pixels.fill((0,0,0))
        # pixels.show()
        time.sleep(0.001)
    
    def close(self):
        pass
        
class Flasher():
    def __init__(self):
        self.flashing = False
        self.flash_color = (255,150,0)
        self.off_color = (0,0,0)
        self.delay = 0.001
        self.isOn = False
        self.isClosed = False

    def beat(self):
        if self.isClosed:
           return
        self.isOn = not self.isOn
        if self.isOn:
            pixels.fill(self.flash_color)
        else:
            pixels.fill(self.off_color)
        pixels.show()
        time.sleep(self.delay)
    
    def close(self):
        self.isOn = False
        self.isClosed = True
        pixels.fill(self.off_color)
        pixels.show()

class Circler():
    def __init__(self):
        self.state = 0
        self.on_color = (0,200,0)
        self.off_color = (0,0,0)
        self.delay = 0.001
        self.isOn = False
        self.isClosed = False

    def beat(self):
        if self.isClosed:
           return
        self.state = self.state+1
          
        self.isOn = not self.isOn
        if self.isOn:
            pixels.fill(self.flash_color)
        else:
            pixels.fill(self.off_color)
        pixels.show()
        time.sleep(self.delay)
    
    def close(self):
        pixels.fill(self.on_color)
        self.isOn = False
        self.isClosed = True
        pixels.fill(self.off_color)
        pixels.show()

class Crasher():
    def __init__(self,velocity):
        self.num_splotches = 10
        self.min_width = 10
        self.max_width = 30
        self.crash_color = (rescale(velocity,20,100,1,255),0,0)
        self.off_color = (0,0,0)
        self.isClosed = False
        self.crash()

    def get_random_val(self,from_val, to_val):
        r = random.random()
        val = from_val + r*(to_val - from_val)
        if val < from_val:  val = from_val
        if val > to_val: val = to_val
        return int(val)

    def crash(self):
        for i in range(self.num_splotches):
            center = self.get_random_val(0, num_pixels-1)
            window = self.get_random_val(self.min_width, self.max_width)
            for j in range(center-int(window/2), center+int(window/2)):
                p = (center + j) % num_pixels
                if pixels[p] == self.crash_color:
                    pixels[p] = self.off_color
                else:
                    pixels[p] = self.crash_color
    
        pixels.show()

    def beat(self):
        if self.isClosed:
           return
    
    def close(self):
        self.isOn = False
        self.isClosed = True
        pixels.fill(self.off_color)
        pixels.show()

class Collector(threading.Thread):
    def __init__(self, device, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.port = port
        self.portName = device.getPortName(port)
        self.device = device
        self.quit = False

    def spread(self,value, max, start, end):
        return start + (value/max)*(end-start)

    def spread_acc(self,value, max, start, end, acc):
        return start + math.pow(value/max, acc)*(end-start)

    def run(self):
        global effect
        self.device.openPort(self.port)
        self.device.ignoreTypes(True, False, True)
        while True:
            if self.quit:
                return
            msg = self.device.getMessage()
            if msg:
                note = msg.getNoteNumber()
                vel = msg.getVelocity()
                if msg.isNoteOn():
                    print(note,vel)
                    if note == 67:
                        effect.close()
                        effect = Crasher(vel)
                    if note == 72:
                        effect.close()
                        effect = Flasher()
                if msg.isNoteOff():
                    effect.close()
                    effect = NoEffect()

effect = NoEffect()
for i in range(dev.getPortCount()):
    device = rtmidi.RtMidiIn()
    
    name = dev.getPortName(i)
    print("PORT: " + name)
    
    if "UM-ONE" in name:
        collector = Collector(device, i)
        collector.start()
        collectors.append(collector)

isOn = False
while True:
    effect.beat()

for c in collectors:
    c.quit = True
