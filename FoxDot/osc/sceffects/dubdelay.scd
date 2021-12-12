SynthDef.new(\dubdelay, {
	arg bus, dubd, dublen, dubwidth, dubfeed, feedback;
	var osc, dry, left, right, magic;
	osc = In.ar(bus, 2);
	dry = osc;
	// Not existing Fb replaced with FBSineL. Please check
	osc = osc + FBSineL({ arg feedback,
		magic = LeakDC.ar(feedback*dubfeed + osc);
		magic = HPF.ar(magic, 400);
		magic = LPF.ar(magic, 5000);
		magic = magic.tanh;
		left = magic;
		right = magic;
		magic = [DelayC.ar(left, 1, LFNoise2.ar(12).range(0,dubwidth)), DelayC.ar(right, 1, LFNoise2.ar(12).range(dubwidth,0))].reverse;	}
	,dublen);
	osc = SelectX.ar(dubd, [dry, osc]);
ReplaceOut.ar(bus, osc)}).add;