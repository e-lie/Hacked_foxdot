from FoxDot import Clock, nextBar, inf, linvar
from ..Instruments import project

def change_bpm(bpm, midi_nudge=True, nudge_base=0.72):
    Clock.bpm = bpm
    project.bpm = bpm

    @nextBar()
    def nudging():
        if midi_nudge:
            Clock.midi_nudge = 60 / bpm - nudge_base
