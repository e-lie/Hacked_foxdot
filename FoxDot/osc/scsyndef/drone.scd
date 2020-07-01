SynthDef.new(\drone, {
	|bus = 0, speed = 1, amp = 1, pan=0, sus = 1, dur = 1, freq=0, gate=1, hpf=40, fmod=0, vib=0|
	var osc, sig, env;
	freq = In.kr(bus, 1);
	freq = [freq, freq+fmod];
	sig = LFNoise1;
	env = EnvGen.ar(Env.linen(0.1,sus,0.1, 1, curve:'lin'),gate,doneAction:0);
	osc = HPF.ar(FreeVerb2.ar(*XFade2.ar(SinOscFB.ar([freq,freq],sig.ar(speed*2)+1),SinOscFB.ar([freq,freq + fmod],sig.ar(speed)+vib),sig.ar(80))),hpf);
	osc = LeakDC.ar((osc * 1.1).tanh, 0.999);
	osc = (osc * env) * amp;
	osc  = Mix(osc) * 0.4;
	osc = Limiter.ar(osc, 0.99);
	osc = Pan2.ar(osc * amp, pan);
	ReplaceOut.ar(bus, osc)
}).add;
