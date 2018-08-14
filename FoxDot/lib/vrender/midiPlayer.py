from midiutil.MidiFile import MIDIFile

# Example composition
# [[(60,1,100),(62,1,100),(64,1,100)],[],[(67,2,100)]]

# tempo in BPM

def createMidi(midi_file, composition, tempo=80, instrumentCode=24):
    track    = 0
    channel  = 0
    MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                         # automatically created)
    MyMIDI.addProgramChange(track, channel, -1, instrumentCode)

    time = 0   # In beats
    MyMIDI.addTempo(track,time, tempo)
    for notes in composition:
        for note in notes:
            pitch = note[0]
            duration = note[1]   # In beats
            volume   = note[2] # 0-127, as per the MIDI standard
            time = note[3]

            MyMIDI.addNote(track, channel, pitch, time, duration, volume)

    with open(midi_file, "wb") as output_file:
        MyMIDI.writeFile(output_file)