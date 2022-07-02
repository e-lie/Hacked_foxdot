from FoxDot.lib.Extensions.MidiMapFactory import MidiMapFactory
from FoxDot.lib.Extensions.DynamicReaperParams import get_reaper_object_and_param_name, set_reaper_param, split_param_name
from FoxDot.lib.Midi import AbletonOut
from FoxDot.lib.Patterns import Pattern


class ReaperInstrumentFacade:

    def __init__(self, clock, reaproject, presets, track_name, midi_channel, midi_map=None, sus=None):

        self._clock = clock
        self._reaproject = reaproject
        self._presets = presets
        self._reatrack = reaproject.get_track(track_name)
        self._midi_channel = midi_channel
        self._sus = sus

    def apply_all_existing_reaper_params(self, reatrack, param_dict, remaining_param_dict={}, runtime_kwargs={}):
        """ This function :
         - tries to apply all parameters in reaper (track fx and send parameters)
         - then send the rest to FoxDot to control supercollider"""

        # if there is non default (runtime kwargs) for an fx turn it on (add a new param "fx"_on = True)
        for key, value in runtime_kwargs.items():
            fx_name, rest = split_param_name(key)
            if rest != 'on' and key not in ['dur', 'sus', 'root', 'amp', 'amplify', 'degree', 'scale', 'room', 'crush', 'fmod']:
                param_dict[fx_name+'_on'] = True

        for param_fullname, value in param_dict.items():
            rea_object, name = get_reaper_object_and_param_name(reatrack, param_fullname)
            if rea_object is not None:  # means param exists in reaper
                set_reaper_param(reatrack, param_fullname, value, update_freq=0.05)
            else:
                remaining_param_dict[param_fullname] = value


    def out(self, *args, sus=None, **kwargs):

        config_defaults = {}

        if "track_default" in self._presets.keys():
            config_defaults = self._presets["track_default"]

        preset_name = self._reatrack.name + "_default"
        if preset_name in self._presets.keys():
            config_defaults = config_defaults | self._presets[preset_name]

        for fx_name in self._reatrack.reafxs.keys():
            preset_name = fx_name + "_default"
            #by default all fxs are off
            config_defaults[fx_name+'_on'] = False
            if preset_name in self._presets.keys():
                config_defaults = config_defaults | self._presets[preset_name]

        params = config_defaults | kwargs  # overwrite gathered default config with runtime arguments

        remaining_param_dict = {}
        self.apply_all_existing_reaper_params(self._reatrack, params, remaining_param_dict, runtime_kwargs=kwargs)

        midi_map_name = remaining_param_dict["midi_map"] if "midi_map" in remaining_param_dict else None
        remaining_param_dict["midi_map"] = MidiMapFactory.generate_midimap(midi_map_name)

        # to avoid midi event collision between start and end note (which prevent the instrument from playing)
        dur = remaining_param_dict["dur"] if "dur" in remaining_param_dict.keys() else 1
        sus = Pattern(sus) if sus is not None else Pattern(dur)-0.03


        return AbletonOut(
            reatrack=self._reatrack,
            channel=self._midi_channel - 1,
            sus=sus,
            *args,
            **remaining_param_dict,
        )


