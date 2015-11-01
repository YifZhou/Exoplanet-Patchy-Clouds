# Referee report reply

## Major comment:

> At the beginning of Sec 4 the authors claim that the photometry 'showed apparently sinusoidal modulations'. They proceed to fit sinusoids to the light curve to determine a period and find periods between 9 and 10 hours. I would argue that this is a dubious approach. The first sensible step is to actually prove that a period is present in the data (in addition to the subjective eye test), before modeling the light curve with a sinusoid.

>As argument in favor of their period detection the authors say that the fitted periods are 'very different from all timescales present in our observations' - that is true, except for ONE timescale, the total duration of the observations, which is around 9 hours. Playing devil's advocate, fitting a sinusoid to a light curve with just a linear trend tends to result in a period around the total length of the dataset. Looking at the light curves, it is not so evident to me that a periodic curve is necessarily the best model - a linear fit would make much sense too, particularly when the first orbit is discarded (as the authors argue, the 1st orbit is often unstable). In that case, 10 hours could be the lower limit of the rotation period.

>What I would like to see is a statistical test that confirms that a periodicity is in fact a better fit to the data than a linear trend. Alternatively, the authors could use some of the well established period search routines to bolster the evidence for their detection. Since the rotational modulation is the key result of this paper, it seems prudent to me to not only rely on the eye test, in particular since there is a wealth of analysis routines available for this kind of problem.

>Parts of introduction, discussion, and abstract may need to be revised after verifying the presumed period.
*****
>Sec 4.2: I do not fully understand why the authors add noise to their light curve and THEN fit sinusoids. Why is the noise increased artificially for this procedure? This seems to be a very unusual period finding algorithm.

The minor comment on the period finding algorithm is directly related to the major comment. Therefore we combine our reply to these comments together. 

We agree with the referee that our original fitting method is inappropriate in the way that it artificially adds noise to the light curve. Therefore we did a rigorous MCMC fitting to measure the period and amplitude based on a sinusoidal model. We cannot use normal period search routines (e.g. Fourier analysis, auto-correlation) because the period of the modulation is larger than our observation baseline. We assumed uniform distribution for the period, amplitude and phase of the sinusoid as priors and included period as long as 40 hours as possible solution. We did the fitting for both including and excluding data from the first orbit. Even when the data from the first orbit were excluded, the posterior distributions for the amplitude and period were constraint, though not as well as those for the fitting include the whole dataset. Our measurements for period and amplitude agree within 1-sigma uncertainties with or without using data from the first orbit. Using the posterior distribution of MCMC fitting, we can show the statistical significance of our measurement.


We also added discussion from the perspective of physical viability of the light curve models and explained a sinusoid is the most suitable choice. A complete flat line is a viable physical that would mean no variability is detected. A flat line with non-zero slope is not a physically viable model: we know that 2M1207b is not fainting away or brightening indefinitely. Therefore, a model that is periodic or irregularly variable (but with a constant mean) is a physical model. The simplest of these physically viable non-constant brightness models is a sine wave.

Our fits demonstrate that the constant level (flat line) can be excluded. Of the non-constant physically viable models the sine wave gives a reasonable chi2, but more complex models are not warranted by our data.

We note that, as the referee also pointed out, there is no timescale linked to the observations that would introduce a 9-hour period slope. The fact that the primary’s light curve is constant to a very high accuracy also demonstrates that there is no instrumental sensitivity drift or any similar effect.


The changes of the manuscript include Sec. 4.2 re-writed, substitution of Fig. 4 with MCMC posterior distribution, and expanding the first paragraph of Sec. 6 for above discussion of physical viability.

## Minor comments:

>- Sec 1, end of 2nd paragraph: It might help to say 'comparing to isolated brown dwarfs', to make the sentence clearer.

We added word *isolated* for clarity.

>- Sec 1, end of 3rd paragraph: For the formation scenarios for the 2M1207 system, Lodato et al. (2005) is an important reference.

We added the reference Lodato et. al. (2005)

>- Sec 1, penultimate paragraph: I would like to see some references for the 'discovery of additional planetary-mass companions' (although they are given earlier in this section).

References for AB pic b and HR8799bcde were added as examples of additional PMC that has red color and under-luminosity problems

>- Sec 2: This is the part that might be a little too concise. One basic information I am missing is the exposure time. It would also help to point out that 1.5 minutes is the MAXIMUM cadence (if I understand this correctly). Also, 'we took 8 SPARS10 exposure sequence' might need a bit more information to help the reader.

We added information for Sec. 2. Exposure time information included, SPARS10, NSAMP=10 are explained. Major modification is the following sentence:

**Original**:In each orbit we took 8 SPARS10 exposure sequence with NSAMP=10, alternating between F160W and F125W filters, with 2--3 identical exposures in each exposure sequence.

**Revised** In each orbit, we took 8 SPARS 10 exposure sequences alternating between F125W and F160W filters. Each sequence contained 2--3 identical exposures that had 10 non-destructive read-outs and total exposure time of 88.4 s.

We added word *maximum* before cadence.

>- Sect 3: I like the innovative approach for modeling the PSF, but I would also like to see this demonstrated in a figure, i.e. an extension of Fig. 1 showing the original image, the correction image, and the two PSFs.

We included the examples of Tiny Tim PSFs as well as the correction map and modified the figure caption correspondingly.

>- Fig 2+3: Information about the epoch of the observations in JD needs to be added, either here or in the text.

JD is added at the beginning of Section 2. 



>- Sec 6, 2nd paragraph: For disk masses, Scholz et al. (2006) is an important
additional reference.

Reference Scholz et. al. (2006) added for disk masses.

>- The discussion in Sec 6 touches on many interesting points, but unfortunately remains relatively vague. At the end of the 2nd paragraph, the authors write 'may place powerful constraints on the evolution of the internal structures of these contracting objects'. Maybe it is worth saying a little more here? What exactly is expected to change in the internal structures of these fully convective objects?

>- For the discussion of the rotational evolution of brown dwarfs, two relevant references that are missing are the PPVI review by Bouvier et al. (see Sect. 4.3.) and, as an update, the recent paper by Scholz, Kostov, et al.. This second paper is important because it contains a large sample of rotation periods for brown dwarfs at about the same age as 2M1207 (although most of them are more massive than 2M1207). At this age some effect of disk braking is still observed, while for the continuing evolution wind braking does play a role in the substellar regime. If 2M1207b really has a rotation period of 10h, it would be a planetary-mass counterpart of the fastest rotating young brown dwarfs. (It would also rotate at a significant fraction of breakup velocity, which might also be of interest.)

We agree with the referee at this point. We expanded the discussion from the point of view of the evolution of angular momentum mainly based on the two references recommended by the referee. We calculated the break-up rotation period is ~2 hr assuming a mass of 5 M_jup and a radius of 1.4 R_jup. The measured rotation period ~10 hr indicates rotation rate is much smaller than the break-up rotation limit.

Scholz et al. 2015 measures rotation period of 20 young brown dwarfs, and compares the BD rotation period measurements from 3 star formation region with rotation evolution tracks based on conservation of angular momentum. The age of brown dwarf in this sample is similar to 2M1207b (~6-9Myr) and the rotation periods of the brown dwarfs in this sample is closer to 2M1207b comparing to Metchev et al. (2015)

We added one paragraph to discuss the comparison of rotation period with BDs, and the evolution of angular momentum of objects with fully convective interior:

**Rotation period of ∼ 10 hour is significantly larger than field brown dwarfs from the sample of Metchev et al. (2015), but comparable to the me- dian period of the sample of Scholz et al. (2015), of which the age is similar to 2M1207b. The rotation period of 2M1207b is agreed within the range predicted by evolutionary track established from measurements of brown dwarfs assuming conservation of angular momentum (Fig. 4 in Scholz et al. (2015)), and much longer than the break-up limit, i.e. the rotation period where the equatorial centrifugal force exceeded gravitational force. Observed rotation rate for brown dwarfs of different ages show little evidence of angular momentum loss at the age of several Myr as oppose to low mass stars (Bouvier et al. 2014; Scholz et al. 2015), and agree with the model of solid body rotation for the fully convective interior. Rotation periods of planetary mass objects with well established age measurement, can place stronger constrain on the internal structure, since angular momentum loss through disks is even less likely comparing with brown dwarfs.**

We added the measurements from Scholz 2015 to left panel of Figure 5. 

>- Sec 7: 'significantly longer than most field BDs with known rotation period'
>- I would advise to be careful with this statement. The available sample of field BD rotation periods is certainly very biased. The vsini data wouldindicate that rotation periods of 10-20 hours may not be that unusual (Reiners& Basri 2008).

Considering the period measurement from sample of Scholz et. al. 2015, We agree with referee at this point.

We modified following sentences in the conclusion.

The period is 10.5 hours, similar to that derived from v sin i measurements for the directly imaged exoplanet β Pic b, significantly longer than most field brown dwarfs with known rotation periods, **but comparable to the brown dwarfs in a sample with similar age to 2M1207b.**

*****

**We include two additional references.**

1. Biller et. al. (2015) (arXiv1510.07625) recently published time resolved observation on PSO J318.5-22, an isolated planetary mass object, and detected variability. We added the reference as an example of time resolved observation and rotational mapping.
2. Karalidi et. al. (2015) published a rotational mapping code that retrieve 2D atmospheric structure from light curves. We added one paragraph at the end of discussion section about the possible application of this tool in the future. 


