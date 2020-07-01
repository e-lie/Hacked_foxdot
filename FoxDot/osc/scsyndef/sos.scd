SynthDef.new(\sos, {
	|amp=1, gate=1, rel=1, dur=1, bus=0, freq=0, pan=0, fmod=0, sus=1, vib=0|
    var osc, env, osc1, osc2;
	freq = In.kr(bus, 1);
	osc1 = VarSaw(freq);
	freq = freq + SinOsc.ar(Rand(0, 8));
    env = EnvGen.ar(Env(curve: 'lin',levels: [0, amp, 0],times: (sus * 1.2)), doneAction: 0);
	osc = FreeVerb2.ar(*XFade2.ar(SinOscFB.ar([Rand(1,freq/2),Rand(1,freq/2)],osc1.kr(Rand(1,freq))),
		  SinOscFB.ar([freq * 1.2,freq],osc1.kr(vib+1)+Rand(2, 2000)/2),osc1.kr(0.1)));
	osc2 = SinOscFB;
	osc2 = RLPF.ar(BrownNoise.ar(1), Rand(400, 1600), 0.015,1) * 1;
	osc = (osc + (osc2 * Rand(0, 0.01))) * env * amp;
	osc = BLowShelf.ar(osc, 60)*0.5;
	osc = Pan2.ar(osc, pan).tanh;
	ReplaceOut.ar(bus,osc);
}).add;