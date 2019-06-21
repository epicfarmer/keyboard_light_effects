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
import time
# from Adafruit_LED_Backpack.SevenSegment import SevenSegment
from SevenSegment import SevenSegment

from keymaps import *
import NoEffect as ne

global graphics_lock
graphics_lock = threading.Lock()

# My Locally defined libraries
import utils

# Global Variables
dev = rtmidi.RtMidiIn()
collectors = []
pixel_pin = board.D18
num_pixels = 300
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
        self.song = 2
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
                print("sb")
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
        self.song = 1+self.song
        self.song = self.song % len(key_map_arrays_by_song)
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
                if "mode" in global_mode_keymap[note]:
                    self.switch_mode(global_mode_keymap[note]["mode"])
                if "song" in global_mode_keymap[note]:
                    self.switch_song()
        elif note in cur_map:
            cur_effect = cur_map[note]
            global graphics_lock
            graphics_lock.acquire()
            effect = cur_effect["effect"](vel, pixels, num_pixels, cur_effect["args"])
            graphics_lock.release()


    def key_released(self,note,mode):
        global effect
        global graphics_lock
        graphics_lock.acquire()
        effect.close()
        effect = ne.NoEffect(pixels,num_pixels)
        graphics_lock.release()

graphics_lock.acquire()
effect = ne.NoEffect(pixels,num_pixels)
graphics_lock.release()

for i in range(dev.getPortCount()):
    device = rtmidi.RtMidiIn()

    name = dev.getPortName(i)
    print("PORT: " + name)

    if "UM-ONE" in name:
        collector = Controller(device, i)
        collector.start()
        collectors.append(collector)

isOn = False
start_time = time.time()
while((time.time() - start_time) < 20):
    graphics_lock.acquire()
    effect.beat()
    pixels.refresh()
    graphics_lock.release()
    time.sleep(0.001)

for c in collectors:
    c.quit = True
