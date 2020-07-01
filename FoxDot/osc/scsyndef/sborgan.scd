SynthDef.new(\sborgan, {
	|bus=0, amp=1, gate=1, atk=0.02, pan=0, spread=0.8, freq=0, sus=1, fmod=0, blur=1|
	var osc1, osc2, osc3, osc, env;
	freq = In.kr(bus, 1);
	sus = sus * blur;
	freq = [freq, freq+fmod];
	freq = SinOsc.ar(freq*\fmfreq.kr(1).lag(0.3)) * \fmrange.kr(0.5).lag(0.3) * LFNoise1.kr(4).range(0.9,1.1) + 1 * freq;
	osc1 = SinOsc.ar(freq.lag(0.1) * [1,8,2,4,1.002]);
	osc2 = LFPulse.ar(freq * [1,4,1.001,2 * LFNoise1.kr(1/20).range(0.999,1.001),1/2], mul:1.82);
	osc = osc1 + osc2;
	osc = osc.fold2(SinOsc.kr(1/13).range(0.7,1));
	osc = osc.wrap2(SinOsc.kr(1/14).range(0.7,1));
	osc = LPF.ar(osc,900)*1;
	osc = HPF.ar(osc, \hpf.kr(80));
	env = EnvGen.ar(Env.perc(level: amp,releaseTime: sus,attackTime: 0.01,curve: 'sin'), doneAction: 0);
	osc = osc.tanh;
	osc = Mix(osc) * 0.25;
	osc = osc * env * amp;
	osc = Pan2.ar(osc,pan);
	ReplaceOut.ar(bus,osc)
}).add;