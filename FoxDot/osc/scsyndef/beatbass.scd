SynthDef.new(\beatbass, {
	arg freq = 0, amp = 1, bus = 0, pan = 0, atk = 0.01, dec = 1, curve = -4, beatFreq = 15;
	var env, osc, osc1, osc2;
	freq = In.kr(bus, 1);
	env = Env.perc(atk,dec,amp,curve).kr(doneAction: 0);
	osc1 = SinOsc.ar(freq);
	osc2 = SinOsc.ar(Line.kr(freq + beatFreq, freq, dec));
	osc = Mix([osc1, osc2]);
	osc = osc * env * amp;
	osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus,osc)
}).add