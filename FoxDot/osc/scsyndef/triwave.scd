SynthDef.new(\triwave,{
	|bus = 0, pan = 0.0, freq = 0, amp = 1.0, atk = 0.01, dec = 0.1, sus = 1, rel = 0.5, lforate = 10, lfowidth = 0.0, cutoff = 300, rq = 0.5|
	var osc1, osc2, vibrato, filter, env, osc;
	freq = In.kr(bus, 1);
	vibrato = SinOsc.ar(lforate, Rand(0, 3.0));
	env = Env.asr(atk, dec, sus, rel).kr(doneAction: 0);
	osc1 = Saw.ar(freq * (1.0 + (lfowidth * vibrato)), 0.5);
	osc2 = Mix(LFTri.ar((freq.cpsmidi + [11.9, 12.1]).midicps));
	osc = RHPF.ar(((osc1 * 0.4) + (osc2 * 0.6)), cutoff, rq);
	osc = osc * env * amp;
	osc = Pan2.ar(osc,pan);
	ReplaceOut.ar(bus,osc)
}).add;