## NOTES:
## Every not should have a timeout after which it will turn off if no key replaces it.
## Every key should have an optional argument to turn off on key release.

## For playing with keyboard
keyboard_toggle = False

import rtmidi
import threading
import board
import neopixel
import numpy as np
import math
# from Adafruit_LED_Backpack.SevenSegment import SevenSegment
from SevenSegment import SevenSegment


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
num_pixels = 32
brightness = 0.7
wait = 0.003
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)
from_wait = 0.2
to_wait = 0.001
max_ti = 10

## Seven segment display dictionary
ssd_dictionary = {
        0:{0x3f},
        1:{0x06},
        2:{0x5b},
        3:{0x4f},
        4:{0x66},
        5:{0x6d},
        6:{0x7d},
        7:{0x07},
        8:{0x7f},
        9:{0x6f}
    }
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
        87:{"effect":de.DictionaryEffect, "args":{"state":"0011000000000000000000000000110O","on_color":(255,0,255)} },
        82:{"effect":de.DictionaryEffect, "args":{"state":"0000111000000000000000000111000O","on_color":(255,0,255)} },
        81:{"effect":de.DictionaryEffect, "args":{"state":"0000000110000000000000011000000O","on_color":(255,0,255)} },
        71:{"effect":de.DictionaryEffect, "args":{"state":"0000000001110000000011100000000O","on_color":(255,0,255)} },
        67:{"effect":de.DictionaryEffect, "args":{"state":"0000000000001100001100000000000O","on_color":(255,0,255)} },
        69:{"effect":de.DictionaryEffect, "args":{"state":"11111111111111111111111111111111","on_color":(250,250,250)} }
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

key_maps_by_mode_clock_song = [
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

key_maps_by_mode_black_hole = [
        keymap_0, # 0
    ];

key_map_arrays_by_song = [
        key_maps_by_mode_clock_song,
        key_maps_by_mode_black_hole
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
        self.display = SevenSegment()
        self.display.begin()
        self.display.clear()
        self.song = 1
        self.switch_song()
        self.global_channel = 15
        self.button_debounce = 10
        # self.increment_button = Button(20,pull_up = True)
        # self.decrement_button = Button(26,pull_up = True)
        # self.reset_button = Button(19,pull_up = True)
        # self.song_switch_button = Button(16,pull_up = True)
        self.previous_increment_state = False
        self.previous_decrement_state = False
        self.previous_reset_state= False
        self.previous_song_switch_state= False

    def test_button(self):
        return
        increment_button_state = self.increment_button.is_pressed
        decrement_button_state = self.decrement_button.is_pressed
        reset_button_state = self.reset_button.is_pressed
        song_switch_button_state = self.song_switch_button.is_pressed
        if increment_button_state:
            self.previous_increment_state = self.previous_increment_state + 1
            if self.previous_increment_state == self.button_debounce:
                print("ib")
                self.switch_mode(self.mode+1)
        else:
            self.previous_increment_state = 0
        if decrement_button_state:
            self.previous_decrement_state = self.previous_decrement_state + 1
            if self.previous_decrement_state == self.button_debounce:
                print("db")
                self.switch_mode(self.mode-1)
        else:
            self.previous_decrement_state = 0
        if reset_button_state:
            self.previous_reset_state = self.previous_reset_state + 1
            if self.previous_reset_state == self.button_debounce:
                print("rb")
                self.switch_mode(0)
        else:
            self.previous_reset_state = 0
        if song_switch_button_state:
            self.previous_song_switch_state = self.previous_song_switch_state + 1
            if self.previous_song_switch_state == self.button_debounce:
                print("ssb")
                self.switch_song()
        else:
            self.previous_song_switch_state = 0

    def switch_mode(self,d):
        d = d % len(key_map_arrays_by_song[self.song])
        self.mode = d
        print("Activating Mode " + str(d))
        self.display.set_digit(2,math.floor(d/10))
        self.display.set_digit(3,d % 10)
        self.display.write_display()
        ## Enable Mode Light

    def switch_song(self):
        self.song = 1-self.song
        self.switch_mode(0)
        self.display.set_digit(0,self.song)
        self.display.write_display()
        print("Activating Song " + str(self.song))
        ## Enable Song Light

    def run(self):
        global effect
        self.device.openPort(self.port)
        self.device.ignoreTypes(True, False, True)
        while True:
            self.test_button()
            msg = self.device.getMessage()
            if msg:
                note = msg.getNoteNumber()
                vel = msg.getVelocity()
                chn = msg.getChannel()
                self.global_key = False
                toggle = False
                if chn == 6:
                    toggle = True
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

        # cur_map = key_maps_by_mode[self.mode]
        cur_map = key_map_arrays_by_song[self.song][self.mode]
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
    pixels.refresh()

for c in collectors:
    c.quit = True
