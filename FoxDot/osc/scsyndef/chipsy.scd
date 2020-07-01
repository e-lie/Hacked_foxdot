SynthDef.new(\chipsy, {
	|bus = 0, freq = 0, amp = 1, pan = 0|
	var osc, env;
	freq = In.kr(bus, 1);
	env = Env.perc(0.02, 0.1).kr(doneAction: 0);
	osc = Mix(LFPulse.ar(freq: freq * [1, 5/2], iphase: 0.0, width: 0.5, mul: amp));
	osc = osc * env ;
	osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus,osc)
}).add;
