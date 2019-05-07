import sys
import rtmidi
import threading
import time
import board
import neopixel
import math
import random

# My Locally defined libraries
import utils
import NoEffect as ne
import FlashEffect as fe
import CrashEffect as cre
import CircleEffect as cie

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

        



class Collector(threading.Thread):
    def __init__(self, device, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.port = port
        self.portName = device.getPortName(port)
        self.device = device
        self.quit = False
        self.circle_state = 0

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
                        effect = cre.CrashEffect(vel,pixels,num_pixels)
                    if note == 68:
                        effect.close()
                        self.circle_state = self.circle_state + 1
                        effect = cie.CircleEffect(vel,pixels,num_pixels,self.circle_state)
                    if note == 72:
                        effect.close()
                        effect = fe.FlashEffect(pixels,num_pixels)
                if msg.isNoteOff():
                    effect.close()
                    effect = ne.NoEffect(pixels,num_pixels)

effect = ne.NoEffect(pixels,num_pixels)
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
