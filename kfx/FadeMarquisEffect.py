import time
import color
import numpy as np
import math

class FadeMarquisEffect():
    def __init__(self,velocity,pixels,n_pixels,args):
        self.flashing = False
        self.color1 = (155,255,155)
        self.color2 = (0,0,0)
        self.delay = 0.001
        self.isOn = False
        self.isClosed = False
        self.pixels = pixels
        self.n_pixels = n_pixels
        self.start = time.time()
        self.total_seconds = 4.
        self.period_seconds = .005
        self.separation = 5
        
        if "color1" in args:
            self.color1 = args["color1"]
        if "color2" in args:
            self.color2 = args["color2"]
        if "transition_time" in args:
            self.total_seconds = args["transition_time"]
        if "period" in args:
            self.period_seconds = args["period"]
        if "n_period" in args:
            self.period_seconds = self.total_second / args["n_period"]
        if "separation" in args:
            self.separation = args["separation"]

        self.time_0_pixels = np.arange(self.n_pixels/(self.separation + 1))*(self.separation+1)

    def beat(self):
        elapsed = time.time() - self.start # Need Paul
        # print("%f seconds" % elapsed)
        if self.isClosed:
           return
        if elapsed >= self.total_seconds:
            self.pixels.fill((0,0,0))
            self.pixels.show()
            return
        out_color = color.rescale(
                self.color1,
                self.color2,
                1-elapsed/self.total_seconds
                )
        for j in ((self.time_0_pixels + math.floor(elapsed / self.period_seconds)) % self.n_pixels):
            self.pixels[int(j)] = out_color
        self.pixels.show()
        for j in ((self.time_0_pixels + math.floor(elapsed / self.period_seconds)) % self.n_pixels):
            self.pixels[int(j)-1] = (0,0,0)
        self.pixels.show()
        time.sleep(self.delay)

    
    def close(self):
        self.isOn = False
        self.isClosed = True
        self.pixels.fill(self.color2)
        self.pixels.show()

