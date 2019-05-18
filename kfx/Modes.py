import piplates.RELAYplate as RELAY
import rtmidi
import threading
import board
import neopixel
import RPi.GPIO as GPIO
from gpiozero import LED


# My Locally defined libraries
import utils
import NoEffect as ne
import FlashEffect as fe
import CrashEffect as cre
import CircleEffect as cie
import DictionaryEffect as de

# Global Variables
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

pinout_dict = [
        "",
        "3V",
        "5V",
        2,
        "5V",
        3,
        "Ground",
        4,
        14, 
        "Ground",
        15, 
        17, # Mode 0 +
        18,
        27, # Mode 1 +
        "Ground",
        22, # Mode 2 + 
        23,
        "3V",
        24,
        10, # Mode 3 +
        "Ground",
        9, # Mode 4 +
        25,
        11, # Mode 5 +
        8,
        "Ground",
        7,
        "SD",
        "SC",
        5,
        "Ground",
        6,
        12,
        13,
        "Ground",
        19,
        16,
        26,
        20,
        "Ground",
        21
        ]

key_dict = {
        'test' : 1
        }


# PINOUT Setup for LEDs
GPIO.setup(pinout_dict[11],GPIO.OUT) # 0 HIGH
GPIO.setup(pinout_dict[12],GPIO.OUT) # 0 LOW
GPIO.setup(pinout_dict[13],GPIO.OUT) # 1 HIGH
GPIO.setup(pinout_dict[15],GPIO.OUT) # 2 HIGH
GPIO.setup(pinout_dict[16],GPIO.OUT) # 2 LOW
GPIO.setup(pinout_dict[19],GPIO.OUT) # 4 HIGH
GPIO.setup(pinout_dict[21],GPIO.OUT) # 5 HIGH
GPIO.setup(pinout_dict[22],GPIO.OUT) # 5 LOW
GPIO.setup(pinout_dict[23],GPIO.OUT) # 6 HIGH
GPIO.setup(pinout_dict[24],GPIO.OUT) # 6 LOW
GPIO.output(pinout_dict[11],0)
GPIO.output(pinout_dict[12],0)
GPIO.output(pinout_dict[13],0)
GPIO.output(pinout_dict[15],0)
GPIO.output(pinout_dict[16],0)
GPIO.output(pinout_dict[19],0)
GPIO.output(pinout_dict[21],0)
GPIO.output(pinout_dict[22],0)
GPIO.output(pinout_dict[23],0)
GPIO.output(pinout_dict[24],0)

mode0_keymap = {
        89:{"effect":cie.CircleEffect, "state":0 },
        82:{"effect":cie.CircleEffect, "state":1 },
        81:{"effect":cie.CircleEffect, "state":2 },
        71:{"effect":cie.CircleEffect, "state":3 },
        67:{"effect":cie.CircleEffect, "state":4 },
        62:{"effect":cie.CircleEffect, "state":5 },
        72:{"effect":cie.CircleEffect, "state":6 }
        }

key_maps = [mode0_keymap];



class Controller(threading.Thread):
    def __init__(self, device, port):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.port = port
        self.portName = device.getPortName(port)
        self.device = device
        self.quit = False
        self.circle_state = 0
        self.mode = 0


    def mode_to_pin(self,mode):
        if mode > 5:
            print("Mode should be between 0 and 6 inclusive")
            return
        if mode == 0:
            return(11)
        if mode == 1:
            return(13)
        if mode == 2:
            return(15)
        if mode == 3:
            return(19)
        if mode == 4:
            return(21)
        if mode == 5:
            return(23)


    def switch_mode(self,d):
        old_pin = self.mode_to_pin(self.mode)
        self.mode = d
        pin = self.mode_to_pin(self.mode)
        print("Activating Mode "+str(d))
        print("  Old Pin: " +str(old_pin))
        print("  Pin: " +str(pin))

        self.set_low(old_pin)
        self.set_high(pin)


    def set_high(self,pin):       #  TO DO:  Change to use standard gpiozero LED class and led.on functions
        pin = pinout_dict[pin]    #          also change method to "on" and "off"
        print(pin)
        if(isinstance(pin,str)):
            return
        
        GPIO.output(pin,1)


    def set_low(self,pin):
        pin = pinout_dict[pin]
        print(pin)
        if(isinstance(pin,str)):
            return
        GPIO.output(pin,0)


    def run(self):
        global effect
        self.device.openPort(self.port)
        self.device.ignoreTypes(True, False, True)
        while True:
            msg = self.device.getMessage()
            if msg:
                note = msg.getNoteNumber()
                vel = msg.getVelocity()
                chn = msg.getChannel()
                toggle = False
                if chn == 7:
                    print(chn)
                    toggle = True
                if chn == 9:
                    print(chn)
                    toggle = True
                if chn == 14:
                    print(chn)
                    toggle = True
                if toggle != True:
                    continue
                if msg.isNoteOn():
                    self.key_pressed(note,vel,self.mode)
                if msg.isNoteOff():
                    self.key_released(note,self.mode)


    def key_pressed(self,note,vel,mode):
        global effect
        print(note,vel)
        #if note == 103:
            #self.switch_mode(5)
        #if note == 101:
            #self.switch_mode(4)
        #if note == 100:
            #self.switch_mode(3)
        #if note == 98:
            #self.switch_mode(2)
        #if note == 96:
            #self.switch_mode(1)
        #if note == 95:
            #self.switch_mode(0)

        cur_map = key_maps[self.mode]
        if note in cur_map:
            cur_efect = cur_map[note]
            cur_effect.effect(vel, pixels, num_pixels, cur_effect.state)

        if mode == 0:
            if note == 89:
                effect.close()
                effect = cie.CircleEffect(vel,pixels,num_pixels,0)
            if note == 87:
                effect.close()
                effect = cie.CircleEffect(vel,pixels,num_pixels,1)
            if note == 82:
                effect.close()
                effect = cie.CircleEffect(vel,pixels,num_pixels,2)
            if note == 81:
                effect.close()
                effect = cie.CircleEffect(vel,pixels,num_pixels,3)
            if note == 71:
                effect.close()
                effect = cie.CircleEffect(vel,pixels,num_pixels,4)
            if note == 67:
                effect.close()
                effect = cie.CircleEffect(vel,pixels,num_pixels,5)
            if note == 62:
                effect.close()
                effect = cie.CircleEffect(vel,pixels,num_pixels,6)
            if note == 72:
                effect.close()
                effect = fe.FlashEffect(pixels,num_pixels)
        if mode == 1:
            print(note,vel)
            if note == 67:
                effect.close()
                effect = cre.CrashEffect(vel,pixels,num_pixels)
            if note == 68:
                effect.close()
                effect = cie.CircleEffect(vel,pixels,num_pixels,0)
            if note == 69:
                effect.close()
                effect = cie.CircleEffect(vel,pixels,num_pixels,1)
            if note == 70:
                effect.close()
                effect = cie.CircleEffect(vel,pixels,num_pixels,2)
            if note == 71:
                effect.close()
                effect = cie.CircleEffect(vel,pixels,num_pixels,3)
            if note == 72:
                effect.close()
                effect = cie.CircleEffect(vel,pixels,num_pixels,4)
            if note == 73:
                effect.close()
                effect = cie.CircleEffect(vel,pixels,num_pixels,5)
            if note == 74:
                effect.close()
                effect = cie.CircleEffect(vel,pixels,num_pixels,6)
            if note == 75:
                effect.close()
                effect = cie.CircleEffect(vel,pixels,num_pixels,7)
            if note == 76:
                effect.close()
                effect = fe.FlashEffect(pixels,num_pixels)
        if mode == 2:
            print(note,vel)
            if note == 67:
                effect.close()
                effect = de.DictionaryEffect(vel,pixels,num_pixels,30232345)
            if note == 68:
                effect.close()
                effect = de.DictionaryEffect(vel,pixels,num_pixels,0)
            if note == 69:
                effect.close()
                effect = de.DictionaryEffect(vel,pixels,num_pixels,1)
            if note == 70:
                effect.close()
                effect = de.DictionaryEffect(vel,pixels,num_pixels,2)
            if note == 71:
                effect.close()
                effect = de.DictionaryEffect(vel,pixels,num_pixels,3)
            if note == 72:
                effect.close()
                effect = de.DictionaryEffect(vel,pixels,num_pixels,4)
            if note == 73:
                effect.close()
                effect = de.DictionaryEffect(vel,pixels,num_pixels,5)
            if note == 74:
                effect.close()
                effect = de.DictionaryEffect(vel,pixels,num_pixels,6)
            if note == 75:
                effect.close()
                effect = de.DictionaryEffect(vel,pixels,num_pixels,7)
            if note == 76:
                effect.close()
                effect = de.DictionaryEffect(vel,pixels,num_pixels,8)
    def key_released(self,note,mode):
        global effect
        effect.close()
        effect = ne.NoEffect(pixels,num_pixels)

effect = ne.NoEffect(pixels,num_pixels)
for i in range(dev.getPortCount()):
    device = rtmidi.RtMidiIn()
    
    name = dev.getPortName(i)
    print("PORT: " + name)
    
    if "UM-ONE" in name:
        collector = Controller(device, i)
        collector.start()
        collectors.append(collector)

isOn = False
while True:
    effect.beat()

for c in collectors:
    c.quit = True
