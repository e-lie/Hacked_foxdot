SynthDef.new(\garfield, {
	|bus=0, freq=0, mult=3, amp=1, pan=0, gate=1, atk=0.01, sus=1, phase=0, para1=0.5, vibrato=1, fmod=0.3|
	var env, osc, del;
	freq = In.kr(bus,1);
	freq = [freq,freq+fmod];
	env = Env.linen(atk,sus,0.2,curve:\sin).kr(doneAction:0);
	del = SinOsc.ar(1/8, phase, mult);
	osc = SinOscFB.ar(freq, 0.3, add: SinOsc.ar(vibrato));
	osc = CrossoverDistortion.ar(osc, 0.8, para1);
	osc = RLPF.ar(osc, 2800) + osc;
	osc = CombN.ar(osc, 0.39, 0.085);
	osc = Splay.ar(osc);
	osc = Mix(osc);
	osc = LeakDC.ar(Limiter.ar(osc,1));
	osc = osc * env * amp;
	osc = Pan2.ar(osc,pan).tanh;
	ReplaceOut.ar(bus,osc);
}).add;
