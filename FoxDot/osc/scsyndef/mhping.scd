SynthDef.new(\mhping,{
	|freq = 0, amp = 1, atk = 0.001, sus=1, rel=0.3, curve = -16, pan = 0, bus = 0, rate = 9, depth = 0.02|
	var osc, lfo, env;
	freq = In.kr(bus, 1);
	lfo = LFNoise2.ar(rate).range(1/(1 + depth),(1 + depth));
	env = Env.linen(attackTime: atk, sustainTime: sus, releaseTime: rel, curve: curve).kr(doneAction:0);
	osc = SinOsc.ar(freq: [freq, freq * lfo], mul: env);
	osc = osc * env * amp;
	osc = Pan2.ar(osc,pan);
	ReplaceOut.ar(bus,osc)
}).add;
