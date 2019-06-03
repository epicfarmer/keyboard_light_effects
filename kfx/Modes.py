## NOTES:
## Every not should have a timeout after which it will turn off if no key replaces it.
## Every key should have an optional argument to turn off on key release.

## For playing with keyboard
keyboard_toggle = False

import piplates.RELAYplate as RELAY
import rtmidi
import threading
import board
import neopixel
import RPi.GPIO as GPIO
import numpy as np
from gpiozero import LED


# My Locally defined libraries
import utils
import NoEffect as ne
import FlashEffect as fe
import CrashEffect as cre
import CircleEffect as cie
import DictionaryEffect as de
import FadeMarquisEffect as fme

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

#         00000000001111111111222222222233
#         01234567890123456789012345678901
#"state":"11000000000000000000000000000011"
#"state":"0011000000000000000000000000110O"
#"state":"0000111000000000000000000111000O"
#"state":"0000000110000000000000011000000O"
#"state":"0000000001110000000011100000000O"
#"state":"0000000000001100001100000000000O"
#"state":"11111111111111111111111111111111"

# This code is an attempt at fitting mode changes into this part
global_mode_keymap = {
        60:{"mode":0},
        61:{"mode":1},
        62:{"mode":2},
        63:{"mode":3},
        64:{"mode":4},
        65:{"mode":5},
        66:{"mode":6},
        67:{"mode":7},
        68:{"mode":8},
        69:{"mode":9},
        70:{"mode":10},
        71:{"mode":11},
        72:{"mode":12},
        73:{"mode":13},
        74:{"mode":14},
        75:{"mode":15},
        76:{"mode":16},
        77:{"mode":17},
        78:{"mode":18},
        79:{"mode":19},
        80:{"mode":20},
        }


## debug_global_mode
keymap_0 = {
        89:{"effect":de.DictionaryEffect, "args":{"state":"11000000000000000000000000000011","on_color":(255,0,255)} },
        87:{"effect":de.DictionaryEffect, "args":{"state":"0011000000000000000000000000110O"} },
        82:{"effect":de.DictionaryEffect, "args":{"state":"0000111000000000000000000111000O"} },
        81:{"effect":de.DictionaryEffect, "args":{"state":"0000000110000000000000011000000O"} },
        71:{"effect":de.DictionaryEffect, "args":{"state":"0000000001110000000011100000000O"} },
        67:{"effect":de.DictionaryEffect, "args":{"state":"0000000000001100001100000000000O"} },
        69:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111"} }
        }

keymap_1 = {
        72:{"effect":de.DictionaryEffect, "args":{"state":"00001111111100000000111111110000"} },
        80:{"effect":de.DictionaryEffect, "args":{"state":"11111111000000001111111100000000"} },
        68:{"effect":de.DictionaryEffect, "args":{"state":"00000000111111110000000011111111"} },
        77:{"effect":de.DictionaryEffect, "args":{"state":"11110000000011111111000000001111"} },
        79:{
            "effect":fme.FadeMarquisEffect,
            "args":{
                "transition_time" : 3.5,
                "color1" : (155,255,155),
                "color2" : (0,0,0)
                } 
            }
        }

keymap_2 = {
        98:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"01000000000000100000100000100010",
                "on_color":(0,125,0)
                }
            },
        97:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"01000100000100100010100010100010",
                "on_color":(0,110,50)
                }
            },
        94:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"11010100001100100010100110101010",
                "on_color":(0,100,80)
                }
            },
        84:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"11010101001100101110100110101110",
                "on_color":(0,80,100)
                }
            },
        83:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"11011101101110101110101110111110",
                "on_color":(0,50,110)
                }
            },
        82:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"11011111101110111110111111111110",
                "on_color":(0,0,125)
                }
            },
        72:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"11111111111111111111111111111111",
                "on_color":(255,0,0)
                }
            }
        }

keymap_3 = {
        69:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"10000000000000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        74:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"01000000000000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        79:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"00100000000000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        82:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"00010000000000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        80:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"00001000000000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        85:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"00000100000000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        65:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"00000010000000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        68:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"00000001000000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        87:{
            "effect":de.DictionaryEffect,
            "args":{
                "state":"00000000100000000000000000000000",
                "on_color":(0,125,0)
                }
            },
        59:{
            "effect":fe.FlashEffect,
            "args":{
                "state":"00000000100000000000000000000000",
                "on_color":(125,125,0)
                }
            },
        50:{
            "effect":fe.FlashEffect,
            "args":{
                "state":"00000000100000000000000000000000",
                "on_color":(0,125,125)
                }
            },
        }

keymap_4 = {
        }

keymap_5 = {
        "86": {
            "effect":cre.CrashEffect,
            "args":{
                "state":"00000000100000000000000000000000",
                "on_color":(0,125,125)
                }
            }
        }

keymap_6 = {

        }

keymap_7 = {

        }

keymap_8 = {

        }

keymap_9 = {

        }

key_maps_by_mode = [
        keymap_0, # 0
        keymap_1, # 1
        keymap_2, # 2
        keymap_0, # 3
        keymap_3, # 4
        keymap_4, # 5
        keymap_0, # 6
        keymap_3, # 7
        keymap_9, # 8  # 3 pulses of clusters of notes
        keymap_5, # 9  #
        keymap_6, # 10 
        keymap_0, # 11
        keymap_3, # 12
        keymap_7, # 13 # Modified for synth
        keymap_8, # 14 # Modified for synth
        keymap_8, # 15 # Modified for synth
        ];

key_maps_by_mode = [
        keymap_0, # 0
        keymap_1, # 1
        keymap_2, # 2
        keymap_0, # 3
        keymap_3, # 4
        keymap_4, # 5
        keymap_0, # 6
        keymap_3, # 7
        keymap_9, # 8  # 3 pulses of clusters of notes
        keymap_5, # 9  #
        keymap_6, # 10 
        keymap_0, # 11
        keymap_3, # 12
        keymap_7, # 13 # Modified for synth
        keymap_8, # 14 # Modified for synth
        keymap_8, # 15 # Modified for synth
        ];

if keyboard_toggle:
    key_maps_by_mode[0] = {
        89:{"effect":de.DictionaryEffect, "args":{"state":"11000000000000000000000000000011","on_color":(255,0,255)} },
        79:{
            "effect":fme.FadeMarquisEffect,
            "args":{
                "transition_time" : 3.5,
                "color1" : (155,255,155),
                "color2" : (0,0,0)
            } 
        }
    }



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
        self.global_channel = 15


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
        # old_pin = self.mode_to_pin(self.mode)
        self.mode = d
        # pin = self.mode_to_pin(self.mode)
        print("Activating Mode " + str(d))
        # print("  Old Pin: " + str(old_pin))
        # print("  Pin: " + str(pin))
        # self.set_low(old_pin)
        # self.set_high(pin)


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
                self.global_key = False
                toggle = False
                if chn == 7:
                    toggle = True
                if chn == 9:
                    toggle = True
                if chn == 14:
                    toggle = True
                if chn == self.global_channel:
                    self.global_key = True
                    toggle = True
                if keyboard_toggle: ## Just for practice with keyboard
                    toggle = True
                if toggle != True:
                    continue
                if msg.isNoteOn():
                    self.key_pressed(note,vel,self.mode)
                if msg.isNoteOff():
                    self.key_released(note,self.mode)


    def key_pressed(self,note,vel,mode):
        global effect
        print("Note", note,vel)

        cur_map = key_maps_by_mode[self.mode]
        if self.global_key:
            if note in global_mode_keymap:
                self.switch_mode(global_mode_keymap[note]["mode"])
        elif note in cur_map:
            cur_effect = cur_map[note]
            effect = cur_effect["effect"](vel, pixels, num_pixels, cur_effect["args"])


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




