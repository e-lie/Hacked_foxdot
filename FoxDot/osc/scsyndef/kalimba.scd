SynthDef.new(\kalimba, {
	|bus=0, freq=0, amp=1, pan=0, mix=0.1, relMin=2.5, relMax=3.5|
	var osc, env;
	freq = In.kr(bus, 1);
	osc = SinOsc.ar(freq);
	env = EnvGen.ar(Env.perc(0.005, Rand(relMin, relMax), 1, -8), doneAction: 0);
	osc = osc * env;
	osc = (osc * (1 - mix)) + (DynKlank.ar(`[
		[240*ExpRand(0.9, 1.1), 2020*ExpRand(0.9, 1.1), 3151*ExpRand(0.9, 1.1)],
		[-7, 0, 3].dbamp,
		[0.8, 0.05, 0.07]
		], PinkNoise.ar * EnvGen.ar(Env.perc(0.001, 0.01))) * mix);
	osc =  Pan2.ar(osc, pan, amp);
	ReplaceOut.ar(bus,osc)
}).add;
