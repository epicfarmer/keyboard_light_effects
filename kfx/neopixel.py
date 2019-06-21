import threadsafe_tkinter as tkinter
import math
import threading
import time

class NeoPixel():
    def __init__(self, pixel_pin, num_pixels, auto_write):
        self.top = tkinter.Tk()
        self.num_pixels = num_pixels
        self.diameter = 500
        self.radius = math.floor(self.diameter / 2)
        self.canvas_size = math.floor(self.diameter * 1.2)
        self.canvas_center = math.floor(self.canvas_size / 2)
        self.led_radius = 3

        self.canvas = tkinter.Canvas(self.top, bg="black", height = self.canvas_size,width=self.canvas_size)
        self.canvas.pack()
        self.slice_size = math.pi*2 / self.num_pixels
        self.leds = []
        for i in range(0,self.num_pixels):
            this_angle = 3 * math.pi/2 + self.slice_size*i
            this_x = int(math.cos(this_angle) * self.radius + self.canvas_center)
            this_y = int(math.sin(this_angle) * self.radius + self.canvas_center)
            # this_box = (
            #     this_x - self.led_radius,
            #     this_y - self.led_radius,
            #     this_x + self.led_radius,
            #     this_y + self.led_radius
            # )
            self.leds.append(self.canvas.create_oval(
                this_x - self.led_radius,
                this_y - self.led_radius,
                this_x + self.led_radius,
                this_y + self.led_radius,
                fill = "black"
            ))
        self.events = []
        self.fill((0,0,0))
        self.refresh()

    def show(self):
        while len(self.events) > 0:
            event = self.events.pop(0)
            event()
        self.events.append(lambda:time.sleep(0.001))

    def refresh(self):
        for j in range(0, self.num_pixels):
            tmp = self[j]
            if(len(tmp) > 6):
                r = int(tmp[1:3],16)
                g = int(tmp[3:5],16)
                b = int(tmp[5:7],16)
                # if (g > 0 & g < 255):
                #     print((r,g,b))
        self.top.update()

    def color_rgb(self,r,g,b):
        return "#%2X%2X%2X" % (r,g,b)

    def color(self,t):
        return "#%02X%02X%02X" % (t[0], t[1], t[2])

    def fill(self,this_color):
        for i in range(0, self.num_pixels):
            self[i] = this_color
        self.events.append(lambda:print("Filling with",self.color(this_color)))
        # self.events.append(lambda:time.sleep(0.01))

    def __getitem__(self, key):
        this_color = self.canvas.itemcget(key, "fill")
        return(this_color)

    def __setitem__(self, key, val):
        self.events.append(lambda:self.canvas.itemconfig(self.leds[key],fill=self.color(val)))
