SynthDef.new(\chipsy, {
	|bus = 0, freq = 0, amp = 1, atk = 0.001, sus=1, rel=0.009, pan = 0|
	var osc, env;
	freq = In.kr(bus, 1);
	env = Env.linen(atk,sus,rel,curve:\lin).kr(doneAction: 0);
	osc = Mix(LFPulse.ar(freq: freq * [1, 5/2], iphase: 0.01, width: 0.5)).tanh;
	osc = osc * env * amp;
	osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus,osc)
}).add;
