SynthDef.new(\gbell, {
	|bus = 0, freq = 0, t60=8, pitchy=1, amp=1, pan = 0|
	var osc, env, exciter;
	freq = In.kr(bus, 1);
	env = Env.perc(0.01, 0.02, curve:\sin).kr(doneAction:0);
	exciter = WhiteNoise.ar() * env * 0.03;
	osc = DynKlank.ar(
		`[
			[1, 2, 2.803, 3.871, 5.074, 7.81, 10.948, 14.421],   // freqs
			[1, 0.044, 0.891, 0.0891, 0.794, 0.1, 0.281, 0.079], // amplitudes
			[1, 0.205, 1, 0.196, 0.339, 0.047, 0.058, 0.047]*t60     // ring times
		],exciter,freqscale: freq);
	DetectSilence.ar(osc, 0.001, 0.75, doneAction:2);
	osc = Pan2.ar(osc,pan,amp);
	Out.ar(bus,osc);
}).add;
