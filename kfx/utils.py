def rescale(value,min,max,omin,omax):
    print(value,min,max,omin,omax)
    value = (omax - omin) * (value - min)/(max- min) + omin
    if value < omin:
      value = omin
    if value > omax:
      value = omax
    return(int(value))

def print_message(midi, port):
    if midi.isNoteOn():
        print('%s: ON: ' % port, midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
    elif midi.isNoteOff():
        print('%s: OFF:' % port, midi.getMidiNoteName(midi.getNoteNumber()))
    elif midi.isController():
        print('%s: CONTROLLER' % port, midi.getControllerNumber(), midi.getControllerValue())
   
    print(midi)


