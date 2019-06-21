import mxm.midifile as midi
import time
import threading

from mxm.midifile.src import constants as c
from mxm.midifile.src.midi_events import MidiEvents

class MidiToEvents(MidiEvents):

    def __init__(self):
        super().__init__()
        self.time = 0
        self.events = []

    def getEvents(self):
        return(self.events)

    def getPortName(self,port):
        return(0)

    def openPort(self,port):
        pass

    def ignoreTypes(self,a,b,c):
        pass

    def getMessage(self):
        pass

    def getPortCount(self):
        return(1)


    #############################
    # channel events

    def note_on(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
         self.events.append((self.time,channel,note,velocity,True))

    def note_off(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        self.events.append((self.time,channel,note,velocity,False))

    def update_time(self,new_time,relative):
        # print(relative)
        self.time = self.time + new_time

    # #########################

class RtMidiIn():
    def __init__(self):
        super().__init__()
        filename = "/home/jkaminsky/Downloads/07 Clock Song-46-all-instruments.mid"
        filename = "/home/jkaminsky/Downloads/07 Clock Song-46-synth-and-modes.mid"
        import mxm.midifile as midi
        a = MidiToEvents()
        b = midi.MidiInFile(a,filename)

        a.getMessage()
        b.read()
        self.events = a.getEvents()
        ## For testing:
        self.events = [
                [762000,6,89,100,True],
                [762200,6,89,100,False],
                [762400,6,87,100,True],
                [762600,6,87,100,False],
                [762800,6,82,100,True],
                [763000,6,82,100,False],
                [763200,6,81,100,True],
                [763400,6,81,100,False],
                [763600,6,71,100,True],
                [763800,6,71,100,False],
                [764000,6,67,100,True],
                [764200,6,67,100,False],
                [764400,6,69,100,True],
                [764600,6,69,100,False],

        ]
        self.start_time = time.time()
        self.last_time = time.time() - 1
        self.event_index = 0

    def getPortName(self,port):
        return("UM-ONE Fake")

    def openPort(self,port):
        pass

    def ignoreTypes(self,a,b,c):
        pass

    def getMessage(self):
        current_time = (time.time() - self.start_time)* 200 + 762000
        if(len(self.events) > self.event_index):
            if(self.events[self.event_index][0] < current_time):
                self.event_index = self.event_index + 1
                print(self.events[self.event_index - 1])
                return(Message(
                    self.events[self.event_index-1][1],
                    self.events[self.event_index-1][2],
                    self.events[self.event_index-1][3],
                    self.events[self.event_index-1][4]
                    ))

    def getPortCount(self):
        return(1)


class Message():
    def __init__(self,channel,note,velocity,on):
        self.channel = channel
        self.note = note
        self.velocity = velocity
        self.on = on
    def getNoteNumber(self):
        return(self.note)
    def getVelocity(self):
        return(self.velocity)
    def getChannel(self):
        return(self.channel)
    def isNoteOn(self):
        return(self.on)
    def isNoteOff(self):
        return(not self.on)


if __name__ == "__main__":
    filename = "/home/jkaminsky/Downloads/07 Clock Song-46-all-instruments.mid"
    import mxm.midifile as midi
    print("Start")
    test = RtMidiIn()
    while(True):
        tmp = test.getMessage()
        if tmp:
            print(tmp.getNoteNumber())
            print(tmp.getVelocity())
            print(tmp.getChannel())
            print(tmp.isNoteOff())
            print(tmp.isNoteOn())
    print("Finish")
