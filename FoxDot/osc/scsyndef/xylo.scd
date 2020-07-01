SynthDef.new(\xylo, {
	|bus = 0,freq = 0, t60=1.8, amp=1, gate=1, pan = 0|
	var osc, exciter;
	freq = In.kr(bus, 1);
	exciter = WhiteNoise.ar() * EnvGen.ar(Env.perc(0.001, 0.05), gate) * 0.06;
	osc = DynKlank.ar(
		`[
			[1, 2, 2.803, 3.871, 5.074, 7.81, 10.948, 14.421],   // freqs
			[1, 0.044, 0.891, 0.0891, 0.794, 0.1, 0.281, 0.079], // amplitudes
			[1, 0.205, 1, 0.196, 0.339, 0.047, 0.058, 0.047]*t60     // ring times
		],
		exciter,freq);
	osc = osc * amp;
	DetectSilence.ar(osc, 0.001, 0.5, doneAction:0);
	osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus,osc)
}).add;