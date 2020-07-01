SynthDef.new(\rlead, {
	|bus = 0, freq=0, amp=1, gate=1, bps=2, pan = 0|
    var osc, env, seq;
	freq = In.kr(bus, 1);
    seq = Demand.kr(Impulse.kr(bps*4), 0, Dseq(freq*[1,3,2], inf)).lag(0.02);
    osc = LFSaw.ar(freq*{rrand(0.995, 1.005)}!2);
    osc = Splay.ar(osc,2,center:pan);
    osc = MoogFF.ar(osc, seq, 0.2);
	env = EnvGen.ar(Env.asr(0.01,1,0.01),gate, doneAction:0);
    osc = osc * env * amp/2;
	osc = Pan2.ar(osc,pan);
	ReplaceOut.ar(bus,osc)
}).add;