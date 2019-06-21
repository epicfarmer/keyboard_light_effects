class SevenSegment():
    def __init__(self):
        self.values = [None,None,None,None]
        pass
    def begin(self):
        pass
    def clear(self):
        self.values = [None,None,None,None]
    def set_digit(self,idx,val):
        self.values[idx] = val
    def write_display(self):
        print(self.values)
