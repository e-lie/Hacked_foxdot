SynthDef.new(\bphase, {
	|bus = 0, freq = 0, atk = 0.02, amp=1, sus = 1, rel = 0.3, pan = 0|
	var osc, env, osc1, osc2;
	freq = In.kr(bus, 1);
	osc1 = PMOsc;
	osc2 = SinOsc;
	env = EnvGen.ar(Env.linen(atk, sus, rel, curve: \lin), doneAction:0);
	osc = osc1.ar(osc2.kr(0.1,freq),freq/2 + osc2.kr(freq * 0.06, pi), 2, osc1.ar(4,2,1,0,osc1.ar(freq*0.04,2,1)), osc2.kr(0.2));
	osc = Mix.ar(osc);
	osc = osc * env * amp;
	osc = Pan2.ar(osc,pan);
	ReplaceOut.ar(bus,osc)
}).add;