import time
import utils
import color
import math

class CircleEffect():
    def __init__(self,velocity,pixels,n_pixels,args):
        self.off_color = (0,0,0)
        self.delay = 0.001
        self.num_states = 7
        self.state = args["state"]
        self.isOn = False
        self.isClosed = False
        self.pixels = pixels
        self.n_pixels = n_pixels
        self.state = self.state % self.num_states

        self.on_color = color.rescale((0,255,0),(0,0,255),self.state/(self.num_states-1))
        # self.scaled_val_1 = utils.rescale(self.state,0,self.num_states,1,255)
        # self.scaled_val_2 = utils.rescale(self.num_states - self.state,0,self.num_states,1,255)

        # self.on_color= (0,self.scaled_val_2,self.scaled_val_1)
        self.num_states = self.num_states - 1

        if(self.state == self.num_states):
            self.pixels.fill(self.on_color)
            self.pixels.show()
            return

        npu = math.floor(self.n_pixels * (self.state + 1)/ self.num_states)
        npl = math.floor(self.n_pixels * self.state / self.num_states)
        np = npu - npl
        # print(self.state)
        # print(npl,npu,np)
        for j in range(np):
            p = math.floor((self.state / self.num_states) * self.n_pixels) + j
            # print(p/self.n_pixels)
            self.pixels[p] = self.on_color
        self.pixels.show()

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
