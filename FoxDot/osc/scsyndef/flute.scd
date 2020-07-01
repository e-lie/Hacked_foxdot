SynthDef.new(\flute, {
	|bus=0, pan= 0, scl = 0.3, freq = 0, press = 0.87, breath = 0.06, feedbk1 = 0.4, feedbk2 = 0.4, dur = 1, gate = 1, amp = 1|
	var env1, env2, envibr, vibr, sr, cr, block, poly, ifqc, osc;
	var flow1, sum1, sum2, fqc, temp1, ax, sum3, value, temp2, flute1, fdbckArray;
	sr = SampleRate.ir;
	cr = ControlRate.ir;
	block = cr.reciprocal;
	freq = In.kr(bus, 1);
	ifqc = freq;
	env1 = EnvGen.kr(Env.new([ 0.0, 1.1 * press, press, press, 0.0 ], [ 0.06, 0.2, dur - 0.46, 0.2 ], 'lin' ));
	env2 = EnvGen.kr(Env.new([ 0.0, amp, amp, 0.0 ], [ 0.1, dur - 0.02, 0.1 ], 'lin' ), doneAction: 0);
	envibr = EnvGen.kr(Env.new( [ 0.0, 0.0, 1, 1, 0.0 ], [ 0.5, 0.5, dur - 1.5, 0.5 ], 'lin') );
	flow1 = LFClipNoise.ar( sr, env1 );
	vibr = SinOsc.ar( 4, 0, 0.1 * envibr );
	sum1 = ( breath * flow1 ) + env1 + vibr;
	fqc = ifqc.reciprocal - ( sum1/20000 ) - ( 9/sr ) + ( ifqc/12000000 ) - block;
	fdbckArray = LocalIn.ar(1);
	flute1 = fdbckArray;
	sum2 = sum1 + ( flute1 * feedbk1 );
	ax = DelayC.ar( sum2, ifqc.reciprocal - block * 0.5, fqc * 0.5 - ( sum1/ifqc/cr ) + 0.001 );
	poly = ax - ( ax.cubed );
	sum3 = poly + ( flute1 * feedbk2 );
	value = LPF.ar(sum3,2000);
	flute1 = DelayC.ar( value, ifqc.reciprocal - block, fqc );
	fdbckArray = flute1;
	LocalOut.ar(fdbckArray);
	osc = value*env2*amp;
	osc = Pan2.ar(osc,pan);
	ReplaceOut.ar(bus, osc)
}).add;
