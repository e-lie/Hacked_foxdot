SynthDef.new(\garfield, {
	|bus=0, freq=0, mult=4, amp=1, pan=0, gate=1, rel= 1, dur=1, phase=0, para1=0.3, vib=1, fmod=0|
	var env, osc, del;
	freq = In.kr(bus,1);
	freq = [freq,freq+fmod];
	env =  EnvGen.ar(Env.linen(0.0,dur,0),doneAction:0);
	del =  SinOsc.ar(1/8, phase, mult);
	osc =  SinOscFB.ar(freq, del, add: SinOsc.ar(vib));
	osc = CrossoverDistortion.ar(osc, 0.8, para1);
	osc = RLPF.ar(osc, 2800, mul:amp) + osc;
	osc = CombN.ar(osc, 0.39, 0.085);
	osc = Splay.ar(osc);
	//osc = Mix(osc);
	osc = osc * env * amp;
	osc = LeakDC.ar(Limiter.ar(osc, 1));
	osc = Pan2.ar(osc,pan).tanh;
	ReplaceOut.ar(bus,osc);
}).add;