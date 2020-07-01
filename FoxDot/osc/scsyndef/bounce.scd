SynthDef.new(\bounce, {
	arg para1=2, bus=0, para2=2.5, gate=1, amp=1, pan=0, freq=0, sus=1, fmod=0;
	var env, osc;
	freq = In.kr(bus, 1);
	freq = [freq,freq+fmod];
	osc = CombN.ar(Decay2.ar(Impulse.ar([[para1,para2],0.5])) * Blip.ar(freq,4));
	env = EnvGen.ar(Env.adsr(0.005,0.1,0.8,0.1), gate=1, doneAction:0);
	osc = osc * env;
	osc = Mix(osc) * 0.125;
	osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc * amp)
}).add;
