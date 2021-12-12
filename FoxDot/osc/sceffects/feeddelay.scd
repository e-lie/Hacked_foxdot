SynthDef.new(\feeddelay, {
	arg bus, feed, feedfreq, feedback;
	var osc,out;
	osc = In.ar(bus, 2);
	//Not existing Fb replaced with FBSineL. Please check
	out = osc + FBSineL({osc = CombN.ar(HPF.ar(feedback*feed, feedfreq) + osc, 0.5, 0.25).tanh;	},0.5,0.125);
ReplaceOut.ar(bus, osc)}).add;