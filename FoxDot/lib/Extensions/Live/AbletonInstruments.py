from typing import Mapping

from FoxDot.lib.Extensions.Live.MidiMapFactory import MidiMapFactory
from FoxDot.lib.Extensions.PyliveSmartParams import get_device_and_param_name, set_smart_param
from FoxDot.lib.Scale import Scale
from FoxDot.lib.Midi import AbletonOut
from FoxDot.lib.Patterns import Pattern


class AbletonInstrumentFacade:

    default_degree = [0]
    default_scale = Scale.default
    default_oct = 3
    default_amp = 1

    def __init__(self, clock, smart_set, track_name, channel, grouping=False, oct=None, amp=None, midi_map=None, config={}, scale=None, set_defaults=True, dur=1, sus=None):
        self._clock = clock
        self._smart_set = smart_set
        self._smart_track = getattr(smart_set, track_name)
        self._channel = channel
        self._grouping = grouping
        self._oct = oct if oct else self.default_oct
        self._dur = dur
        self._sus = sus
        self._amp = amp if amp else self.default_amp
        self._config = config
        self._scale = scale if scale is not None else self.default_scale
        self._midi_map = MidiMapFactory.generate_midimap(midi_map)

    def apply_all_existing_live_params(self, smart_track, param_dict, remaining_param_dict={}):
        for param_fullname, value in param_dict.items():
            device, name = get_device_and_param_name(smart_track, param_fullname)
            if device is not None: # means param exists in live
                set_smart_param(smart_track, param_fullname, value, update_freq=0.05)
            else:
                remaining_param_dict[param_fullname] = value

    def out(self, *args, channel=None, oct=None, scale=None, midi_map=None, dur=None, sus=None, amp=None, **kwargs):
        midi_map = midi_map if midi_map else self._midi_map
        channel = channel if channel else self._channel
        channel_suffix = "_" + str(channel)
        oct = oct if oct else self._oct
        dur = dur if dur else self._dur
        amp = amp if amp is not None else self._amp
        scale = scale if scale is not None else self._scale
        sus = sus if sus else self._sus
        # to avoid midi event collision between start and end note (which prevent the instrument from playing)
        sus = Pattern(sus) if sus is not None else Pattern(dur)-0.03

        params = self._config | kwargs  # overwrite base config with runtime arguments
        live_params = params

        if self._grouping:  # handle per instrument parameters
            group_subtracks = getattr(self._smart_set, channel_suffix).get_pylive_track(
            ).tracks  # get the group named like "_6" for the channel then its subtracks
            # get the names and remove the _6 like channel suffix from the names
            group_track_names = [
                track.name[:-len(channel_suffix)] for track in group_subtracks]
            for track_name in group_track_names:
                track_params = {key.replace(track_name+"_", ""): value for (
                    key, value) in params.items() if track_name in key.split("_")}
                # get the corresponding smart track
                subtrack = getattr(self._smart_set, track_name+channel_suffix)
                self.apply_all_existing_live_params(subtrack, track_params)
                for key in track_params.keys():  # remove per instrument params
                    del params[track_name+"_"+key]

        remaining_param_dict = {}
        self.apply_all_existing_live_params(self._smart_track, params, remaining_param_dict)

        return AbletonOut(
            live_params=live_params,
            smart_track=self._smart_track,
            midi_map=midi_map,
            channel=self._channel-1,
            oct=oct,
            scale=scale,
            dur=dur,
            sus=sus,
            amp=amp,
            *args,
            **remaining_param_dict,
        )


