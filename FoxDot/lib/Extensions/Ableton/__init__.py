import live

from FoxDot.lib import Clock, player_method

from .SmartSetParams import SmartSet
from .AbletonInstruments import AbletonInstrumentFacade

liveset = live.Set()

try:
    liveset.scan(scan_clip_names=True, scan_devices=True)
    smartset = SmartSet(Clock, liveset)
except Exception as err:
    output = err.message if hasattr(err, 'message') else err
    print("Error scanning and initializing  ableton liveset: {output} -> skipping ableton integration".format(output=output))


def arm_all():
    for track in liveset.tracks:
        track.arm = 1

class AbletonInstrumentFactory:

    def __init__(self, config_default):
        self._config_default = config_default

    def create_instruc(self, *args, **kwargs):
        """handle exceptions gracefully especially if corresponding track does not exist in Live"""
        try:
            if "config" in kwargs:
                kwargs["config"] = self._config_default | kwargs["config"]
            else:
                kwargs["config"] = self._config_default
            result = AbletonInstrumentFacade(Clock, smartset, *args, **kwargs)
            return result.out
        except Exception as err:
            output = err.message if hasattr(err, 'message') else err
            print("Error creating instruc {name}: {output} -> skipping".format(name=kwargs["track_name"], output=output))
            return None

@player_method
def vol(self, value):
    smart_track = self.attr["smart_track"][0]
    smart_track.vol = value
    return self

@player_method
def pan(self, value):
    smart_track = self.attr["smart_track"][0]
    smart_track.pan = value
    return self
