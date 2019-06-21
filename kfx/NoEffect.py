import time

class NoEffect():
    def __init__(self,pixels,n_pixels):
        pass

    def beat(self):
        # pixels.fill((0,0,0))
        # pixels.show()
        time.sleep(0.001)
    
    def close(self):
        pass

