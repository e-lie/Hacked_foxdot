SynthDef.new(\wobblebass, {
	|bus=0, amp=1, gate=1, pan=0, spread=0.8, freq=0, atk = 0.01|
	var osc, env, osc1, osc2, osc3;
	freq = In.kr(bus, 1);
	osc1 = LFSaw.ar(freq * 1 + (0.04 * [1,-1]));
	osc2 = LFSaw.ar(freq * 0.99 );
	osc3 = LFSaw.ar(freq * 1 );
	osc = osc1 + osc2 + osc3;
	osc = (osc*40).tanh;
	env = Env.linen(atk,0.1,0.8,0.1).kr(gate: gate,doneAction: 0);
	osc = Splay.ar(osc, spread, amp, pan);
	osc = Pan2.ar(osc,pan);
	ReplaceOut.ar(bus,osc)
}).add;