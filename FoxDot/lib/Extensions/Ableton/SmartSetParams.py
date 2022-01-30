from FoxDot.lib.TimeVar import TimeVar


def normalize_param(param, value):
    if param.maximum == 127:
        return value * 127.0
    else:
        return value * 1.0


def normalize_volume(value):
    """function make volume 1.0 corresponds to gain 0 in ableton (max volume without gain)
    so 1.1 gives the volume some gain"""
    return value * 0.85 if value <= 1.17 else 1.0
    return result


def split_param_name(name):
    if "_" in name:
        splitted = name.split('_')
        device_name = splitted[0]
        param_name = '_'.join(splitted[1:])
        return device_name, param_name
    else:
        raise KeyError("Parameter name not splittable by '_': " + name)

def get_device_and_param_name(smart_track, full_name):
    # device can point to a smart_device or a smart_track (when param is vol or pan)
    if full_name in ['vol', 'pan']:
        device = smart_track
        name = full_name
    else:
        device_name, param_name = split_param_name(full_name)
        if (device_name in smart_track.smart_devices.keys()
            and param_name in smart_track.smart_devices[device_name].param_ids.keys()):
            device = smart_track.smart_devices[device_name]
            name = param_name
        else:
            print("Parameter doesn't exist: " + full_name)
            device, name = None, None
    return device, name


def set_smart_param(clock, smart_track, full_name, value, update_freq=0.05):
    # device can point to a smart_device or a smart_track (when param is vol or pan)
    device, name = get_device_and_param_name(smart_track, full_name)
    if isinstance(value, TimeVar):
        # to update a time varying param and tell the preceding recursion loop to stop
        # we switch between two timevar state old and new alternatively 'timevar1' and 'timevar2'
        if name not in device.__param_states.keys() or device.__param_states[name] != 'timevar1':
            new_state = 'timevar1'
        else:
            new_state = 'timevar2'

        def schedule_futureloop_update(name, value, new_state, update_freq):
            device.__param_states[name] = new_state
            set_param_futureloop(clock, device, name, value, new_state, update_freq)
        # beat=None means schedule for the next bar
        clock.schedule(schedule_futureloop_update, beat=None, args=[name, value, new_state, update_freq])
    else:
        # to switch back to non varying value use the state normal to make the recursion loop stop
        def schedule_value_update(device, name, value):
            device.__param_states[name] = 'normal'
            setattr(device, name, float(value))
        # beat=None means schedule for the next bar
        clock.schedule(schedule_value_update, beat=None, args=[device, name, value])

def set_param_futureloop(clock, device, name, value, state, update_freq):
    if device.__param_states[name] == state:
        setattr(device, name, float(value))
        clock.future(update_freq, set_param_futureloop, args=[clock, device, name, value, state, update_freq])


class SmartSet(object):

    def __init__(self, clock, set):
        self._clock = clock
        self.__set = set
        self.__tracks = set.tracks
        self.__smart_tracks = {}
        self.__track_names = {}
        self.__track_ids = {}
        for id, track in enumerate(self.__tracks):
            simple_name = track.name.lower().replace(' ', '_').replace('/', '_')
            self.__track_names[id] = simple_name
            self.__track_ids[simple_name] = id
            self.__smart_tracks[simple_name] = SmartTrack(
                self._clock, self.__tracks[self.__track_ids[simple_name]])

    def __getattr__(self, name):
        dict_name = '_SmartSet' + name
        if dict_name in self.__dict__.keys():
            return self.__dict__[dict_name]
        else:
            return self.__smart_tracks[name]

    @property
    def vol(self):
        return self.__set.get_master_volume()

    @vol.setter
    def vol(self, value):
        # TODO make this setter TimeVar ready like for smart tracks
        self.__set.set_master_volume(normalize_volume(value))

    @property
    def pan(self):
        return self.__set.get_master_pan()

    @pan.setter
    def pan(self, value):
        self.__set.set_master_pan(value)


class SmartTrack(object):

    def __init__(self, clock, track):
        self._clock = clock
        self.__track = track
        self.__devices = track.devices
        self.__smart_devices = {}
        self.__device_names = {}
        self.__device_ids = {}
        self.__param_states = {}
        for id, device in enumerate(self.__devices):
            simple_name = device.name.lower().replace(' ', '_').replace('/', '_')
            self.__device_names[id] = simple_name
            self.__device_ids[simple_name] = id
            self.__smart_devices[simple_name] = SmartDevice(
                self._clock, self.__devices[self.__device_ids[simple_name]])

    def __getattr__(self, name):
        dict_name = '_SmartTrack' + name
        if dict_name in self.__dict__.keys():
            return self.__dict__[dict_name]
        else:
            return self.__smart_devices[name]

    def get_pylive_track(self):
        return self.__track

    @property
    def device_ids(self):
        return self.__device_ids

    @property
    def devices(self):
        return self.__devices

    @property
    def smart_devices(self):
        return self.__smart_devices

    @property
    def vol(self):
        return self.__track.volume

    @vol.setter
    def vol(self, value):
        self.__track.volume = normalize_volume(value)
        # self.__set_vol(value)

    @property
    def pan(self):
        return self.__track.pan

    @pan.setter
    def pan(self, value):
        self.__track.pan = value
        # self.__set_pan(value)


class SmartDevice(object):

    def __init__(self, clock, device):
        self._clock = clock
        self.__device = device
        self.__params = device.parameters
        self.__param_names = {}
        self.__param_ids = {}
        self.__param_states = {}
        for id, param in enumerate(self.__params):
            simple_name = param.name.lower().replace(' ', '_').replace('/', '_')
            if 'macro' not in simple_name:
                self.__param_names[id] = simple_name
                self.__param_ids[simple_name] = id

    def __getattr__(self, name):
        dict_name = '_SmartDevice' + name
        if dict_name in self.__dict__.keys():
            return self.__dict__[dict_name]
        elif name == 'params':
            return [name for name in self.__param_ids.keys()]
        else:
            return self.__params[self.__param_ids[name]].value

    @property
    def param_ids(self):
        return self.__param_ids

    @property
    def params(self):
        return self.__params

    def __setattr__(self, name, value):
        if name in ['_SmartDevice__device', '_SmartDevice__params', '_SmartDevice__param_names',
                    '_SmartDevice__param_ids', '_SmartDevice__param_states', '_clock']:
            super().__setattr__(name, value)
        else:
            self.__set_param(name, value)

    def __set_param(self, name, value):
        param = self.__params[self.__param_ids[name]]
        param.value = normalize_param(param, value)
