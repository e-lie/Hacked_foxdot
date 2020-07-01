SynthDef.new(\blips, {
	|bus = 0, freq = 0, numharm = 10, atk = 0.01, rel = 1, amp = 1, pan = 0, beatsPercent = 1.001|
	var osc, env;
	freq = In.kr(bus, 1);
	env = Env.perc(atk, rel, amp).kr(doneAction: 0);
	osc = LeakDC.ar(Mix(Blip.ar([freq, freq*beatsPercent], numharm)));
	osc = osc * env * amp;
	osc = Pan2.ar(osc,pan);
	ReplaceOut.ar(bus,osc)
}).add;