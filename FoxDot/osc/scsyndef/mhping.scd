SynthDef.new(\mhping,{
	|freq = 0, amp = 1, dur = 1, atk = 0.001, curve = -3, pan = 0, bus = 0, rate = 7, depth = 0.03|
	var osc, lfo, env;
	freq = In.kr(bus, 1);
	lfo = LFNoise2.ar(rate).range(1 / (1 + depth), (1 + depth));
	env = Env.perc(attackTime: atk, releaseTime: dur, level: amp, curve: curve).kr(doneAction:0);
	osc = SinOsc.ar(freq: [freq, freq * lfo], mul: env);
	osc = osc * env * amp;
	osc = Pan2.ar(osc,pan);
	ReplaceOut.ar(bus,osc)
}).add;