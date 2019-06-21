import threadsafe_tkinter as tkinter
import math
import threading
import time
import matplotlib.pyplot as plt
# import matplotlib.figure as fig

global fix
global ax
fig, ax = plt.subplots()

class NeoPixel():
    def __init__(self, pixel_pin, num_pixels, auto_write):
        self.num_pixels = num_pixels
        self.diameter = 500
        self.radius = math.floor(self.diameter / 2)
        self.canvas_size = math.floor(self.diameter * 1.2)
        self.canvas_center = math.floor(self.canvas_size / 2)
        self.led_radius = 3
        self.slice_size = math.pi*2 / self.num_pixels
        self.my_x = []
        self.my_y = []
        self.events = []
        self.led_colors = []
        for i in range(0,self.num_pixels):
            self.led_colors.append("black")
            this_angle = 3 * math.pi/2 + self.slice_size*i
            self.my_x.append(int(math.cos(this_angle) * self.radius + self.canvas_center))
            self.my_y.append(int(math.sin(this_angle) * self.radius + self.canvas_center))


    def show(self):
        print("Show")
        ax
        ax.clear()
        ax.scatter(self.my_x, self.my_y,c=self.led_colors)
        pass

    def refresh(self):
        plt.pause(0.001)
        pass

    def color_rgb(self,r,g,b):
        return "#%2X%2X%2X" % (r,g,b)

    def color(self,t):
        return "#%02X%02X%02X" % (t[0], t[1], t[2])

    def fill(self,this_color):
        for i in range(0, self.num_pixels):
            self[i] = this_color

    def __getitem__(self, key):
        this_color = self.canvas.itemcget(key, "fill")
        return(this_color)

    def __setitem__(self, key, val):
        self.led_colors[key] = self.color(val)
