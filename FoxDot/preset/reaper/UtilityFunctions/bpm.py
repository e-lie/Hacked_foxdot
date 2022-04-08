
from FoxDot import Clock, nextBar
from FoxDot.lib.Extensions.Livebak import live_set


def change_bpm(bpm, midi_nudge=True, nudge_base=0.22):
    Clock.bpm = bpm
    live_set.tempo = bpm

    @nextBar()
    def nudging():
        if midi_nudge:
            Clock.midi_nudge = 60 / bpm - nudge_base
