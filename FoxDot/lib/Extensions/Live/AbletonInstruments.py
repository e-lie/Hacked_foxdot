from typing import Mapping

from FoxDot.lib.Extensions.Live.MidiMapFactory import MidiMapFactory
from FoxDot.lib.Scale import Scale
from FoxDot.lib.Midi import AbletonOut
from FoxDot.lib.Patterns import Pattern


class AbletonInstrumentFacade:

    default_degree = [0]
    default_scale = Scale.default
    default_oct = 3
    default_amp = 1

    def __init__(self, clock, smart_set, presets, track_name, midi_channel, oct=None, amp=None, midi_map=None, config={}, scale=None, dur=1, sus=None):
        self._clock = clock
        self._smart_set = smart_set
        self._presets = presets
        self._smart_track = smart_set.get_track(track_name)
        self._midi_channel = midi_channel
        self._oct = oct if oct else self.default_oct
        self._dur = dur
        self._sus = sus
        self._amp = amp if amp else self.default_amp
        self._config = config
        self._scale = scale if scale is not None else self.default_scale
        self._midi_map = MidiMapFactory.generate_midimap(midi_map)

    def apply_all_existing_live_params(self, smart_track, param_dict, remaining_param_dict={}):
        """ This function gather all the params from different sources to apply them
         in ableton live or supercollider.
         - first it gathers all the parameters present in the current presets matching the track name or device name
         - second it merges it with runtime arguments from instrument class and instrument function call (out method)
         - then tries to apply all this in ableton live
         - finally send the preset to FoxDot to control supercollider"""

        config_defaults = {}

        preset_name = smart_track.name + "_default"
        if preset_name in self._presets.keys():
            config_defaults = config_defaults | self._presets[preset_name]

        for device_name in smart_track.smart_devices.keys():
            preset_name = device_name + "_default"
            if preset_name in self._presets.keys():
                config_defaults = config_defaults | self._presets[preset_name]

        param_dict = config_defaults | param_dict

        for param_fullname, value in param_dict.items():
            device, name, _ = smart_track.get_live_object_and_param_name(param_fullname)
            if device is not None:  # means param exists in live
                smart_track.set_smart_param(param_fullname, value, update_freq=0.05)
            else:
                remaining_param_dict[param_fullname] = value

    def out(self, *args, midi_channel=None, oct=None, scale=None, midi_map=None, dur=None, sus=None, amp=None, **kwargs):
        midi_map = midi_map if midi_map else self._midi_map
        midi_channel = midi_channel if midi_channel is not None else self._midi_channel
        oct = oct if oct is not None else self._oct
        dur = dur if dur is not None else self._dur
        amp = amp if amp is not None else self._amp
        scale = scale if scale is not None else self._scale
        # to avoid midi event collision between start and end note (which prevent the instrument from playing)
        sus = Pattern(sus) if sus is not None else Pattern(dur)-0.03

        params = self._config | kwargs  # overwrite base config with runtime arguments
        live_params = params

        remaining_param_dict = {}
        self.apply_all_existing_live_params(self._smart_track, params, remaining_param_dict)

        return AbletonOut(
            live_params=live_params,
            smart_track=self._smart_track,
            midi_map=midi_map,
            channel=midi_channel - 1,
            oct=oct,
            scale=scale,
            dur=dur,
            sus=sus,
            amp=amp,
            *args,
            **remaining_param_dict,
        )


