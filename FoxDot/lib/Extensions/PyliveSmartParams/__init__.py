from enum import Enum
from FoxDot.lib.TimeVar import TimeVar
from pprint import pprint, pformat


class TrackType(Enum):
    SIMPLE = 1
    GROUP = 2
    SUBTRACK = 3


class SmartSet(object):

    send_ids = {}

    def __init__(self, clock, set):
        self._clock = clock
        self.set = set
        self.smart_tracks = {}
        self.simple_tracks = {}
        self.group_tracks = {}
        self.subtracks = {}
        self.sends = {}
        self.gmixer = None
        self.sends_group = None
        self.instrument_tracks = []

        # dict of form -> snake_name: track_index (index in tracks list)
        groups_dict = {group.name.lower().replace(' ', '_').replace('/', '_'): group.index for group in set.groups}

        for id, track in enumerate(self.set.tracks):
            snake_name = track.name.lower().replace(' ', '_').replace('/', '_')
            if snake_name in groups_dict.keys():
                group_subtracks = [subtrack for subtrack in self.set.tracks[groups_dict[snake_name]]]
                smart_subtracks = {
                    subtrack.name.lower().replace(' ', '_').replace('/', '_'): SmartTrack(
                        self._clock,
                        name=subtrack.name.lower().replace(' ', '_').replace('/', '_'),
                        type=TrackType.SUBTRACK,
                        track=subtrack,
                        smart_set=self,
                    )
                    for subtrack in group_subtracks if "mixer" not in subtrack.name
                }
                mixer_track = [mixer_track for mixer_track in group_subtracks if "mixer" in mixer_track.name][0]
                smart_track = SmartTrack(self._clock, name=snake_name, type=TrackType.GROUP, track=mixer_track,
                                         smart_set=self, subtracks=smart_subtracks)
                self.subtracks = self.subtracks | smart_subtracks
                self.group_tracks[snake_name] = smart_track
                self.smart_tracks[snake_name] = smart_track
                for subtrack_name, subtrack in smart_subtracks.items():
                    self.smart_tracks[subtrack_name] = subtrack
            elif snake_name not in self.subtracks.keys() and "mixer_" not in snake_name:
                smart_track = SmartTrack(self._clock, name=snake_name, type=TrackType.SIMPLE, track=track,
                                         smart_set=self)
                self.smart_tracks[snake_name] = smart_track
                self.simple_tracks[snake_name] = smart_track


    def autodetect_tracks(self):
        for name, smart_track in self.simple_tracks.items():
            if name == "mixer":
                self.gmixer = smart_track
            else:
                self.instrument_tracks.append(smart_track)

        if "sends" in self.group_tracks.keys():
            self.sends_group = self.group_tracks["sends"]
            for i, smart_subtrack in enumerate(self.sends_group.subtracks.values()):
                self.sends[smart_subtrack.name] = i


    #def display_set(self):
    #   for simple_track in self.__simple_tracks

    def __repr__(self):
        return "<SmartSet {} \n\n ################ \n\n {}>".format(self.simple_tracks, self.group_tracks)

    def get_track(self, track_name):
        return self.smart_tracks[track_name]

    def set_send_ids(self, send_ids):
        for track in self.smart_tracks.values():
            track.set_send_ids(send_ids)


class SmartTrack(object):

    send_ids = {}

    def __init__(self, clock, track, name: str, type: TrackType, smart_set: SmartSet, subtracks=[]):
        self._clock = clock
        self.__track = track
        self.__smart_set = smart_set
        self.name = name
        self.type = type
        self.config = {}
        self.subtracks = subtracks
        self.__smart_devices = {}
        self.__smart_device_list = []
        self.__param_states = {}
        for id, device in enumerate(self.__track.devices):
            snake_name = device.name.lower().replace(' ', '_').replace('/', '_')
            smart_device = SmartDevice(device)
            self.__smart_devices[snake_name] = smart_device
            self.__smart_device_list.append(smart_device)

    def __repr__(self):
        result = ""
        if self.type == TrackType.GROUP:
            result = "<SmartTrack {} - {} subtracks: {}>".format(self.name, pformat(self.__smart_devices), pformat(self.subtracks))
        else:
            result = "<SmartTrack {} - {}>".format(self.name, pformat(self.__smart_devices))
        return result

    def __getattr__(self, key):
        if key in self.send_ids.keys():
            return self.get_send(self.send_ids[key])
        return self.__dict__[key]

    def __setattr__(self, key, value):
        if key in self.send_ids.keys():
            self.set_send(self.send_ids[key], value)
        elif key == "vol":
            """function make volume 1.0 corresponds to gain 0 in ableton (max volume without gain)
            so 1.1 gives the volume some gain"""
            result = value * 0.85 if value <= 1.17 else 1.0
            self.__track.volume = result
        elif key == "pan":
            self.__track.pan = value
        else:
            self.__dict__[key] = value

    def set_send_ids(self, send_ids):
        self.send_ids = send_ids

    @classmethod
    def split_param_name(cls, name):
        if "_" in name:
            splitted = name.split('_')
            device_name = splitted[0]
            param_name = '_'.join(splitted[1:])
            return device_name, param_name
        else:
            raise KeyError("Parameter name not splittable by '_': " + name)

    @property
    def vol(self):
        return float(self.__track.volume) / 0.85

    @property
    def pan(self):
        return self.__track.pan

    def get_send(self, send_num):
        return self.__track.get_send(send_num)

    def set_send(self, send_num, value):
        return self.__track.set_send(send_num, value)

    def get_live_track(self):
        return self.__track

    def get_param_states(self):
        return self.__param_states

    def get_live_object_and_param_name(self, param_fullname: str, quiet: bool = False):
        """
        Return object (SmartTrack or SmartDevice) and parameter name to apply modification to.
        Choose usecase (parameter kind : track param like vol, send amount or device param) depending on parameter name.
        This is important to make parameter modification uniform for all cases.
        """
        # device can point to a smart_device or a self (when param is vol or pan)
        live_object, param_name = None, None
        # Track vol or pan
        if param_fullname in ['vol', 'pan']:
            live_object = self
            param_name = param_fullname
            return live_object, param_name, param_fullname
        # Param is a send name
        elif param_fullname in self.send_ids.keys():
            live_object = self
            param_name = param_fullname
            return live_object, param_name, param_fullname
        # Param concerns a subtrack of the group -> recursive call on the subtrack
        elif self.type == TrackType.GROUP and '_' in param_fullname and param_fullname.split('_')[0] in self.subtracks.keys():
            subtrack_name = param_fullname.split('_')[0]
            subtrack = self.subtracks[subtrack_name]
            live_object, param_name, _ = subtrack.get_live_object_and_param_name(param_fullname[len(subtrack_name) + 1:], quiet=quiet)
            return live_object, param_name, param_fullname
        # Param is a device param
        elif '_' in param_fullname:
            first_part, rest = SmartTrack.split_param_name(param_fullname)
            device_names = self.__smart_devices.keys()
            if first_part in device_names:
                device = self.__smart_devices[first_part]
                param_names = device.param_ids.keys()
                if rest in param_names:
                    live_object = self.__smart_devices[first_part]
                    param_name = rest
                    return live_object, param_name, param_fullname
        # If normal name split doesnt work use first device (param name shortcut intru_i_param -> instru_param)
        elif self.__smart_device_list:
            first_device = self.__smart_device_list[0]
            param_names = first_device.param_ids.keys()
            if param_fullname in param_names:
                live_object = self.__smart_device_list[0]
                param_name = param_fullname
                return live_object, param_name, param_fullname
        if not quiet:
            print("Parameter doesn't exist: " + param_fullname)
        return live_object, param_name, param_fullname

    def set_smart_param(self, full_name, value, update_freq=0.05):
        # device can point to a smart_device or a smart track (self) -> (when param is vol or pan)
        device, name, full_name = self.get_live_object_and_param_name(full_name)
        if device is None or name is None:
            return

        self.config = self.config | {full_name: value}
        if isinstance(value, TimeVar):
            # to update a time varying param and tell the preceding recursion loop to stop
            # we switch between two timevar state old and new alternatively 'timevar1' and 'timevar2'
            if name not in device.get_param_states().keys() or device.get_param_states()[name] != 'timevar1':
                new_state = 'timevar1'
            else:
                new_state = 'timevar2'

            def schedule_futureloop_update(name, value, new_state, update_freq):
                device.get_param_states()[name] = new_state
                set_param_futureloop(self._clock, device, name, value, new_state, update_freq)
            # beat=None means schedule for the next bar
            self._clock.schedule(schedule_futureloop_update, beat=None, args=[name, value, new_state, update_freq])
        else:
            # to switch back to non varying value use the state normal to make the recursion loop stop
            def schedule_value_update(device, name, value):
                device.get_param_states()[name] = 'normal'
                setattr(device, name, float(value))
            # beat=None means schedule for the next bar
            self._clock.schedule(schedule_value_update, beat=None, args=[device, name, value])

    def get_smart_param(self, full_name):
        # device can point to a smart_device or a smart track (self) -> (when param is vol or pan)
        device, name, _ = self.get_live_object_and_param_name(full_name)
        if device is None or name is None:
            return
        return getattr(device, name)


def set_param_futureloop(clock, device, name, value, state, update_freq):
    if device.get_param_states()[name] == state:
        setattr(device, name, float(value))
        clock.future(update_freq, set_param_futureloop, args=[clock, device, name, value, state, update_freq])


class SmartDevice(object):

    def __init__(self, device):
        self.__device = device
        self.__params = device.parameters
        self.__param_names = {}
        self.__param_ids = {}
        self.__param_states = {}
        for id, param in enumerate(self.__params):
            snake_name = param.name.lower().replace(' ', '_').replace('/', '_')
            if 'macro' not in snake_name:
                self.__param_names[id] = snake_name
                self.__param_ids[snake_name] = id

    def __getattr__(self, name):
        dict_name = '_SmartDevice__' + name
        if dict_name in self.__dict__.keys():
            return self.__dict__[dict_name]
        else:
            param = self.__params[self.__param_ids[name]]
            return self.get_normalized_param(param)

    def __setattr__(self, name, value):
        if name in ['_SmartDevice__device', '_SmartDevice__params', '_SmartDevice__param_names',
                    '_SmartDevice__param_ids', '_SmartDevice__param_states', '_clock']:
            super().__setattr__(name, value)
        else:
            param = self.__params[self.__param_ids[name]]
            param.value = self.set_normalized_param(param, value)

    def __repr__(self):
        return "<SmartDevice {}>".format(self.__device.name)

    def get_param_states(self):
        return self.__param_states

    def set_normalized_param(self, param, value):
        if param.maximum == 127:
            return value * 127.0
        else:
            return value * 1.0

    def get_normalized_param(self, param):
        if param.maximum == 127:
            return param.value[3] / 127.0
        else:
            return param.value[3]
