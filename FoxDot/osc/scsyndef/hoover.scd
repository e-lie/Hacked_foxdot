SynthDef.new(\hoover, {
	|bus=0,freq=0,amp=1,pan=0|
    var osc, bw, delay, decay, env;
	freq = In.kr(bus, 1);
    bw = 1.035;
    osc = { DelayN.ar(Saw.ar(freq * ExpRand(bw, 1 / bw)) + Saw.ar(freq * 0.5 * ExpRand(bw, 1 / bw)), 0.01, Rand(0, 0.01)) }.dup(20);
    osc = (Splay.ar(osc) * 3).atan;
    env = Env.linen(0.01, 1.0).kr(doneAction: 0);
	osc = osc * env;
	osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus,osc)
}).add;
