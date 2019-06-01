import time
import random
import math
import utils

class CrashEffect():
    def __init__(self,velocity,pixels,n_pixels,args):
        self.num_splotches = 10
        self.min_width = 10
        self.max_width = 30
        self.crash_color = (utils.rescale(velocity,20,100,1,255),0,0)
        self.off_color = (0,0,0)
        self.isClosed = False
        self.pixels = pixels
        self.n_pixels=n_pixels
        self.crash()

    def get_random_val(self,from_val, to_val):
        r = random.random()
        val = from_val + r*(to_val - from_val)
        if val < from_val:  val = from_val
        if val > to_val: val = to_val
        return int(val)

    def crash(self):
        for i in range(self.num_splotches):
            center = self.get_random_val(0, self.n_pixels-1)
            window = self.get_random_val(self.min_width, self.max_width)
            for j in range(center-int(window/2), center+int(window/2)):
                p = (center + j) % self.n_pixels
                if self.pixels[p] == self.crash_color:
                    self.pixels[p] = self.off_color
                else:
                    self.pixels[p] = self.crash_color
    
        self.pixels.show()

    def beat(self):
        if self.isClosed:
           return
    
    def close(self):
        self.isOn = False
        self.isClosed = True
        self.pixels.fill(self.off_color)
        self.pixels.show()
