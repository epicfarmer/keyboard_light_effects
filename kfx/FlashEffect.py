import time

class FlashEffect():
    def __init__(self,velocity,pixels,n_pixels,args):
        self.flashing = False
        self.flash_color = (255,150,0)
        self.off_color = (0,0,0)
        self.delay = 0.001
        self.isOn = False
        self.isClosed = False
        self.pixels = pixels

    def beat(self):
        if self.isClosed:
           return
        self.isOn = not self.isOn
        if self.isOn:
            self.pixels.fill(self.flash_color)
        else:
            self.pixels.fill(self.off_color)
        self.pixels.show()
        time.sleep(self.delay)
    
    def close(self):
        self.isOn = False
        self.isClosed = True
        self.pixels.fill(self.off_color)
        self.pixels.show()

