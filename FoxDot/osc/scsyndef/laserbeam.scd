SynthDef.new(\laserbeam, {
	|bus = 0, pan = 0.0, freq = 0, amp = 1, atk = 0.01|
	var osc, freqenv, env;
	freq = In.kr(bus, 1);
	freqenv = EnvGen.ar(Env([4, 0.5, 1, 1], [atk, 0.01, 1.0]));
	env = EnvGen.ar(envelope: Env([0, 1, 0.5, 0.0], [0.02, 0.2, 0.1]),levelScale: amp,doneAction: 0);
	osc = LFTri.ar(freq: freq * freqenv);
	osc = osc * env * amp;
	osc = Pan2.ar(osc,pan);
	ReplaceOut.ar(bus,osc)
}).add;