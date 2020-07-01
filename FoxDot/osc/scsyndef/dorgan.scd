SynthDef.new(\dorgan,{
	|bus = 0, pan = 0.0, freq = 0, amp = 1, gate = 1, atk = 0.01, dec = 0.5, sus = 1, rel = 0.5, lforate = 10, lfowidth = 0.01, cutoff = 100, rq = 0.5|
	var vibrato, filter, env, osc;
	freq = In.kr(bus, 1);
	vibrato = SinOsc.kr(lforate, Rand(0, 2.0));
	freq = freq * [1, 1.9953843530485, 3.0139733629359];
	freq = freq * (1.0 + (lfowidth * vibrato));
	env = EnvGen.ar(Env.linen(atk, sus, rel), gate, doneAction: 0);
	osc = VarSaw.ar(freq,iphase: Rand(0.0, 1.0) ! 2,width: Rand(0.3, 0.5) ! 2, mul: [0.4,0.3,0.1]);
	osc = Mix(osc);
	filter = RLPF.ar(osc, cutoff, rq);
	osc = osc * env * amp;
	osc = Pan2.ar(osc,pan);
	ReplaceOut.ar(bus,osc)
}).add;