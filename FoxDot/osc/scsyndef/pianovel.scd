SynthDef.new(\pianovel, {
	|bus=0, freq=0, fmod=0, gate=1, amp=1, velocity=80, hard=0.8, sus=1, blur=1, velhard=0.6, pan=0, vib=0|
	var env, osc;
	freq = In.kr(bus, 1);
	osc = MdaPiano.ar([freq + fmod], gate, release: 0.9, stereo: 0.8, sustain: sus * blur, vel: velocity, hard: hard, velhard: velhard);
	osc = TwoPole.ar(osc, 200,0.5, mul:0.5) + osc/2;
	env = EnvGen.ar(Env(times: [sus],levels: [(amp), (amp)],curve: 'step'), doneAction: 0);
	DetectSilence.ar(osc, 0.01, doneAction:2);
	osc = Mix(osc) * env * amp;
	osc = Pan2.ar(osc,pan);
	ReplaceOut.ar(bus,osc);
}).add;