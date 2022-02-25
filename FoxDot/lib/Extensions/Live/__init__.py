import live

from typing import Mapping

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

    def __init__(self, config_base: Mapping, config_default: Mapping, smart_set: SmartSet) -> None:
        self._config_base = config_base
        self._config_default = config_default
        self._smart_set = smart_set

    def create_instruc(self, *args, set_defaults=True, **kwargs):
        """handle exceptions gracefully especially if corresponding track does not exist in Live"""
        try:
            config = self._config_base
            if set_defaults:
                config = config | self._config_default
            if "config" in kwargs:
                kwargs["config"] = config | kwargs["config"]
            else:
                kwargs["config"] = config
            result = AbletonInstrumentFacade(Clock, self._smart_set, *args, **kwargs)
            return result.out
        except Exception as err:
            output = err.message if hasattr(err, 'message') else err
            print("Error creating instruc {name}: {output} -> skipping".format(name=kwargs["track_name"], output=output))
            return None

    def instruments_to_instanciate(self):

        smset: SmartSet = self._smart_set
        smset.autodetect_tracks()

        instrument_dict = {}

        mixer_kwargs = {
            "track_name": "mixer",
            "midi_channel": -1,
            "set_defaults": False
        }

        instrument_dict["mixer"] = self.create_instruc(**mixer_kwargs)

        smset.set_send_ids(smset.sends)

        sends_kwargs = {
            "track_name": "sends",
            "midi_channel": -1,
            "set_defaults": False
        }
        instrument_dict["sends"] = self.create_instruc(**sends_kwargs)

        for i, track in enumerate(smset.instrument_tracks):
            instrument_kwargs = {
                "track_name": track.name,
                "midi_channel": i + 1,
                "set_defaults": False,
                #"scale": Scale.chromatic,
                #"oct": 3,
                #"root": 0,
                #"midi_map": "stdrum",
            }

            instrument_dict[track.name] = self.create_instruc(**instrument_kwargs)

        return instrument_dict

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

@player_method
def get_send(self, send_num):
    if "smart_track" in self.attr.keys():
        smart_track = self.attr["smart_track"][0]
        if isinstance(smart_track, SmartTrack):
            return smart_track.get_send(send_num)

@player_method
def set_send(self, send_num, value):
    if "smart_track" in self.attr.keys():
        smart_track = self.attr["smart_track"][0]
        if isinstance(smart_track, SmartTrack):
            return smart_track.set_send(send_num, value)
