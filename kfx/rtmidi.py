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
        if(channel != 6):
            print(("HERE",channel,note,velocity,use_running_status))
        self.events.append((self.time,channel,note,velocity,True))

    def note_off(self, channel=0, note=0x40, velocity=0x40, use_running_status=False):
        if(channel != 6):
            print(("HERE",channel,note,velocity,use_running_status))
        self.events.append((self.time,channel,note,velocity,False))

    def end_of_track(self):
        self.time = 0;

    def update_time(self,new_time,relative):
        if(relative):
            self.time = self.time + new_time
        else:
            self.time = new_time
        # print(relative)

    # #########################

class RtMidiIn():
    def __init__(self,testing=False):
        super().__init__()
        self.testing = testing
        filename = "/home/jkaminsky/Downloads/07 Clock Song-46-synth-and-modes.mid"
        # filename = "/home/jkaminsky/Downloads/07 Clock Song-46-all-instruments.mid"
        import mxm.midifile as midi
        a = MidiToEvents()
        b = midi.MidiInFile(a,filename)

        a.getMessage()
        b.read()
        self.events = a.getEvents()
        self.sort_events()
        # print(self.events)
        if(self.testing):
            self.events = [
                [762000,15,0,100,True],
                [762000,15,0,100,True],
                [762000,6,61,100,True],
                [762200,6,62,100,True],
                [762400,6,63,100,True],
                [762600,6,64,100,True],
                [762800,6,65,100,True],
                [763000,6,66,100,True],
                [763200,6,67,100,True],
                [763400,6,68,100,True],
                [763600,6,69,100,True],
                [763800,6,70,100,True],
                [764000,6,71,100,True],
                [764200,6,72,100,True],
                [764400,6,73,100,True],
                [764600,6,74,100,True],
                [764800,6,75,100,True],
                [765000,6,76,100,True],
                [765200,6,77,100,True],
                [765400,6,78,100,True],
                [765600,6,79,100,True],
                [765800,6,80,100,True],
                [766000,6,81,100,True],
                [766200,6,82,100,True],
                [766400,6,83,100,True],
                [766600,6,84,100,True],
                [766800,6,85,100,True],
                [767000,6,86,100,True],
                [767200,6,87,100,True],
                [767400,6,88,100,True],
                [767600,6,89,100,True],
                [767800,6,90,100,True],

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

    def sort_events(self):
        self.events = sorted(self.events,key = lambda event:event[0])

    def getMessage(self):
        current_time = (time.time() - self.start_time)* 1000 + 40000
        if(len(self.events) > self.event_index):
            if(self.events[self.event_index][0] < current_time):
                if(self.events[self.event_index][1] != 6):
                    print("HERE")
                self.event_index = self.event_index + 1
                # print(self.events[self.event_index - 1])
                return(Message(
                    self.events[self.event_index-1][1],
                    self.events[self.event_index-1][2],
                    self.events[self.event_index-1][3],
                    self.events[self.event_index-1][4]
                    ))
        else:
            raise(Exception("Song over"))

    def __getitem__(self, key):
        return(self.events[key][0])

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
