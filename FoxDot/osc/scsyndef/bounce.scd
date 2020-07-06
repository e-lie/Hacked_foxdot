SynthDef.new(\bounce, {
	arg para1=2, bus=0, para2=2.5, gate=1, atk=0.005, sus=1, rel=0.09, amp=1, pan=0, freq=0, fmod=0;
	var env, osc;
	freq = In.kr(bus, 1);
	freq = [freq,freq+fmod];
	osc = CombN.ar(Decay2.ar(Impulse.ar([[para1,para2],0.5])) * Blip.ar(freq,4));
	env = Env.linen(atk,sus,rel,curve:\sin).kr(doneAction:0);
	osc = Mix(osc) * 0.5;
	osc = osc * env;
	osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus, osc * amp)
}).add;
