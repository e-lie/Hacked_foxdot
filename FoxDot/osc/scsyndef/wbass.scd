SynthDef.new(\wbass, {
	|bus = 0, freq = 0, gate = 1, amp = 1, pan = 0, atk = 0.01, dec = 0.3, sus = 0.4, rel = 0.1, slideTime = 0.08, cutoff = 1100, width = 0.15, detune = 1.002, preamp = 4|
	var osc, env;
	freq = In.kr(bus, 1);
	env = Env.adsr(atk,dec,sus,rel).kr(gate: gate, doneAction: 0);
	freq = Lag.kr(freq,slideTime);
	osc = VarSaw.ar(freq: [freq, freq * detune], width: width, mul: preamp);
	osc = Mix(osc,0.4).distort;
	osc = LPF.ar(osc, cutoff, amp/2);
	osc = osc * env * amp;
	osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus,osc)
}).add;
