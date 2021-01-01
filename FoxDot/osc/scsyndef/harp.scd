SynthDef.new(\harp,{
	|bus=0, amp=1, freq=0, pan=0, atk=0.01, sus=1, trig=1, decaytime=7, fmod=0, coef=0.04, blend=0.7|
	var osc, env, exciter, root, octave;
	freq = In.kr(bus, 1);
	freq = freq + fmod;
	env = Env.linen(attackTime: atk, sustainTime: decaytime, releaseTime: sus).kr(doneAction: 0);
	exciter = PinkNoise.ar(amp);
    	root = Pluck.ar(  //fundamental
	        in: exciter,
	        trig: trig,
	        maxdelaytime: 0.02, //only change this if freq goes below 20hz
	        delaytime: 1 / freq,
	        decaytime: decaytime,
	        coef: coef,
	        mul: blend
        );
	octave = Pluck.ar(  //octave up
	        in: exciter,
	        trig: trig,
	        maxdelaytime: 0.02, //only change this if freq goes below 20hz
	        delaytime: 1/(2*freq),
	        decaytime: decaytime,
	        coef: coef,
	        mul: (1 - blend)
        );
	osc = Mix.ar(root + octave);
	osc = osc * env;
    DetectSilence.ar(in: osc, doneAction: 2);
	osc = Pan2.ar(osc, pan);
	ReplaceOut.ar(bus,osc)
}).add;
