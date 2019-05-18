import time
import utils
import math

class DictionaryEffect():
    def __init__(self,velocity,pixels,n_pixels,state):
        self.off_color = (0,0,0)
        self.delay = 0.001
        self.num_states = 2^32
        self.state = state
        self.isOn = False
        self.isClosed = False
        self.pixels = pixels
        self.n_pixels = n_pixels
        self.state = self.state % self.num_states
        
        # self.on_color= (0,self.scaled_val_2,self.scaled_val_1)
        self.on_color= (255,0,255)
        self.num_states = self.num_states - 1
        
        for i in range(32):
            if(math.floor(state / (2**i)) % 2 == 1):
                print(i)
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
        self.state = self.state+1
        time.sleep(self.delay)
    
    def close(self):
        self.isOn = False
        self.isClosed = True
        self.pixels.fill(self.off_color)
        self.pixels.show()
