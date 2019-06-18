import tkinter
import math
import threading
from time import sleep

class NeoPixel():
    def __init__(self, pixel_pin, num_pixels, auto_write):
        self.diameter = 500
        self.radius = math.floor(self.diameter / 2)
        self.canvas_size = math.floor(self.diameter * 1.2)
        self.canvas_center = math.floor(self.canvas_size / 2)
        self.led_radius = 3

        self.top = tkinter.Tk()
        self.canvas = tkinter.Canvas(top, bg="black", height = canvas_size,width=canvas_size)
        self.canvas.pack()
        self.slice_size = math.pi*2 / self.num_pixels
        self.leds = []
        for i in range(0,self.num_pixels):
            this_angle = 3 * math.py/2 + self.slice_size[i]
            this_x = int(math.cos(this_angle) * self.radius + self.canvas_center)
            this_y = int(math.sin(this_angle) * self.radius + self.canvas_center)
            this_box = (
                this_x - self.led_radius,
                this_y - self.led_radius,
                this_x + self.led_radius,
                this_y + self.led_radius
            )
            leds.append(canvas.create_oval(
                this_x - self.led_radius,
                this_y - self.led_radius,
                this_x + self.led_radius,
                this_y + self.led_radius,
                fill = "red"
            ))
    def color_rgb(self,r,g,b):
        return "#%2X%2X%2X" % (r,g,b)

    def color(self,t):
        return "#%2X%2X%2X" % (t[0], t[1], t[2])

    def fill(self,this_color):
        for i in range(0, self.num_pixels):
            self.canvas.itemconfig(self.leds[l], fill = self.color(this_color))

    def __getitem__(self, key):
        this_color = self.canvas.itemcget(i, "fill")
        print(this_color)
        return(this_color)

    def __setitem__(self, key, val):
        self.canvas.itemconfig(self.leds[l], fill = self.color(val))

step = 0
num_steps = 5

colors = [(150, 0, 0), (150, 75, 0), (150,150,0), (200, 200, 100), (255, 255, 255)]

def beat():
    global step
    for l in range(0, num_leds):
        canvas.itemconfig(leds[l], fill=color(colors[(l+step)%num_steps]))
    top.after(beat_ms, beat)
    step += 1

top.after(beat_ms, beat)
top.mainloop()
