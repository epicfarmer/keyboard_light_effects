import time
import utils
import math

class DictionaryEffect():
    def __init__(self,velocity,pixels,n_pixels,args):
        self.off_color = (0,0,0)
        self.delay = 0.01
        self.num_states = 32
        self.isOn = False
        self.isClosed = False
        self.pixels = pixels
        self.n_pixels = n_pixels
        
        self.on_color = (155,155,155)

        if "on_color" in args:
            self.on_color = args["on_color"]
        if "state" in args:
            self.state = args["state"]
        
        for i in range(32):
            if self.state[i] == '1':
                # print(i)
                self.segment(i)
        self.pixels.show()
    def segment(self,idx):
        idx_lower = idx
        idx_upper = idx + 1
        light_lower = math.floor(idx_lower / self.num_states * self.n_pixels)
        light_upper = math.floor(idx_upper / self.num_states * self.n_pixels)
        for i in range(light_lower,light_upper):
            self.pixels[i] = self.on_color

    def beat(self):
        if self.isClosed:
           return
        # self.state = self.state+1
        time.sleep(self.delay)
    
    def close(self):
        self.isOn = False
        self.isClosed = True
        self.pixels.fill(self.off_color)
        self.pixels.show()
