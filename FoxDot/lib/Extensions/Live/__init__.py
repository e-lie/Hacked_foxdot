import live

from FoxDot.lib import Clock, player_method

from FoxDot.lib.Extensions.PyliveSmartParams import SmartSet, SmartTrack
from FoxDot.lib.Extensions.Live.AbletonInstruments import AbletonInstrumentFacade

live_set = live.Set()
smart_set = None

try:
    live_set.scan(scan_clip_names=True, scan_devices=True)
    smart_set = SmartSet(Clock, live_set)
except Exception as err:
    output = err.message if hasattr(err, 'message') else err
    print("Error scanning and initializing  ableton liveset: {output} -> skipping ableton integration".format(output=output))


def arm_all(live_set):
    for track in live_set.tracks:
        track.arm = 1

class AbletonInstrumentFactory:

    def __init__(self, config_default, smart_set):
        self._config_default = config_default
        self._smart_set = smart_set

    def create_instruc(self, *args, set_defaults=True, **kwargs):
        """handle exceptions gracefully especially if corresponding track does not exist in Live"""
        try:
            config_default = self._config_default if set_defaults else {}
            if "config" in kwargs:
                kwargs["config"] = config_default | kwargs["config"]
            else:
                kwargs["config"] = config_default
            result = AbletonInstrumentFacade(Clock, self._smart_set, *args, **kwargs)
            return result.out
        except Exception as err:
            output = err.message if hasattr(err, 'message') else err
            print("Error creating instruc {name}: {output} -> skipping".format(name=kwargs["track_name"], output=output))
            return None

@player_method
def setp(self, param_dict):
    for key, value in param_dict.items():
        setattr(self, key, value)

@player_method
def getp(self, filter = None):
    result = None
    if "smart_track" in self.attr.keys():
        smart_track = self.attr["smart_track"][0]
        if isinstance(smart_track, SmartTrack):
            result = smart_track.config
            if filter is not None:
                result = {key: value for key, value in smart_track.config.items() if filter in key}
            else:
                result = smart_track.config
    return result
