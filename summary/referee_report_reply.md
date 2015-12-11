# Referee report reply

We thank the referee for the constructive and prompt report. In response to the major comment, we carried out an MCMC fit to the data that convincingly supported our previous results; we followed and addressed each of the minor comments, too.

## Major comment:

> At the beginning of Sec 4 the authors claim that the photometry 'showed apparently sinusoidal modulations'. They proceed to fit sinusoids to the light curve to determine a period and find periods between 9 and 10 hours. I would argue that this is a dubious approach. The first sensible step is to actually prove that a period is present in the data (in addition to the subjective eye test), before modeling the light curve with a sinusoid.

>As argument in favor of their period detection the authors say that the fitted periods are 'very different from all timescales present in our observations' - that is true, except for ONE timescale, the total duration of the observations, which is around 9 hours. Playing devil's advocate, fitting a sinusoid to a light curve with just a linear trend tends to result in a period around the total length of the dataset. Looking at the light curves, it is not so evident to me that a periodic curve is necessarily the best model - a linear fit would make much sense too, particularly when the first orbit is discarded (as the authors argue, the 1st orbit is often unstable). In that case, 10 hours could be the lower limit of the rotation period.

>What I would like to see is a statistical test that confirms that a periodicity is in fact a better fit to the data than a linear trend. Alternatively, the authors could use some of the well established period search routines to bolster the evidence for their detection. Since the rotational modulation is the key result of this paper, it seems prudent to me to not only rely on the eye test, in particular since there is a wealth of analysis routines available for this kind of problem.

>Parts of introduction, discussion, and abstract may need to be revised after verifying the presumed period.
*****
>Sec 4.2: I do not fully understand why the authors add noise to their light curve and THEN fit sinusoids. Why is the noise increased artificially for this procedure? This seems to be a very unusual period finding algorithm.

The minor comment on the period finding algorithm is directly related to the major comment. Therefore we combine our reply to these comments together. 

We agree with the referee that our original fitting method artificially amplified the noise. Normal period search routines (e.g. Fourier analysis, auto-correlation) are not applicable because the period of the modulation is larger than our observation baseline. Therefore we carried out a rigorous MCMC fit to measure the period and amplitude based on a sinusoidal model. We assumed uniform distributions for the periods, amplitudes and phases of the sine waves as priors and included period as long as 40 hours as possible solution. We fitted the data with and without the data from the first orbit to quantitatively assess the importance of the less stable data. 

By allowing very long period sine waves, we in effect allow a nearly linear solution (which directly address the major comment of the referee).

A new figure for the posterior distribution of the MCMC fit is shown in Figure 4 in the updated manuscript. 

The new analysis leads to two important results: 

1. The posterior distributions for the period concentrate on ~10 hour and agree with what we found previously. The probability for very long period (P > 15 hour) is negligible. 
2. Even only using data from orbits 2-6, the posterior distributions for the amplitude and period are constrained and show result that agree within 1-sigma with the fit using data from orbits 1-6.

The MCMC analysis and above two results directly address and settle the major comments from the referee. Below we explain our response to the minor comments. 

## Minor comments:

>- Sec 1, end of 2nd paragraph: It might help to say 'comparing to isolated brown dwarfs', to make the sentence clearer.

We added word *isolated* for clarity.

>- Sec 1, end of 3rd paragraph: For the formation scenarios for the 2M1207 system, Lodato et al. (2005) is an important reference.

We added the reference Lodato et. al. (2005)

>- Sec 1, penultimate paragraph: I would like to see some references for the 'discovery of additional planetary-mass companions' (although they are given earlier in this section).

References for AB pic b and HR8799bcde were added as examples of additional PMCs that has red color and under-luminosity problems

>- Sec 2: This is the part that might be a little too concise. One basic information I am missing is the exposure time. It would also help to point out that 1.5 minutes is the MAXIMUM cadence (if I understand this correctly). Also, 'we took 8 SPARS10 exposure sequence' might need a bit more information to help the reader.

We added information for Sec. 2. Exposure time information are included, SPARS10, NSAMP=10 are explained. Major modification is the following sentence:

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

We thank the referee for this excellent point. We expanded the discussion from the point of view of the evolution of angular momentum mainly based on the two references recommended by the referee. We calculated the break-up rotation period is ~2 hr assuming a mass of 5 M_jup and a radius of 1.4 R_jup. The measured rotation period ~10 hr indicates rotation rate is much lower than the break-up rotation limit.

Scholz et al. 2015 measured rotation periods of 20 young brown dwarfs, and compared the BD rotation periods from 3 star-forming regions with rotational evolution tracks based on the conservation of angular momentum. The age of brown dwarfs in this sample is similar to 2M1207b and the rotation periods are closer to that of 2M1207b, in contrast to those of the older brown dwarfs studied in Metchev et al. (2015).

We added one paragraph to Sec. 6 to discuss the comparison of rotation period with BDs, and the evolution of angular momentum of objects with fully convective interior.

We added the measurements from Scholz et al. (2015) to left panel of Figure 5. We also modified the conclusion saying our rotation period measurement is similar to those of brown dwarfs in the sample of Scholz et al. (2015)

>- Sec 7: 'significantly longer than most field BDs with known rotation period'
>- I would advise to be careful with this statement. The available sample of field BD rotation periods is certainly very biased. The vsini data would indicate that rotation periods of 10-20 hours may not be that unusual (Reiners& Basri 2008).


We compared our rotation period with the v sin i measurements from Reiners&Basri (2008). We found that comparing to L-type brown dwarfs in that sample, equatorial rotation speed of 2M1207b is still lower than most of brown dwarfs. We agree with the referee that the available sample can be biased, therefore we emphasize that our comparison is limited to the sample with known rotation periods. 

We added the comparison of rotation rate with L-type brown dwarfs in the sample of Reiners&Basri (2008) in the discussion section.

*****

**We included two additional references.**

1. Biller et. al. (2015) (arXiv1510.07625) recently published time resolved observation on PSO J318.5-22, an isolated planetary mass object, and detected variability. We added the reference as an example of time resolved observation and rotational mapping.
2. Karalidi et. al. (2015) published a rotational mapping code that retrieve 2D atmospheric structure from light curves. We added one paragraph at the end of discussion section about the possible application of this tool in the future. 


