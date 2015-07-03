>1) How do you scale (if you scale) the residuals you subtract?

The residuals are not scaled. I simply took the median of the
residuals that have the same dither position and position angle, and
subtracted the median combination from the original images. Since The
chisq distribution of the fitting looks very reasonable for me, I did
not attempt to make further adjustment of the residual models.

> 2) How do the residuals images look like? What is the relative fraction of the light that is not subtracted well?     
> 3) When you calculate the brightness of the sources, how do you use
> the information of the residuals and the TinyTim-based PSF?

These are very important points. However I did not deal with them very
carefully in my previous fit. As I showed in our previous discussion,
Tinytim does not provide a precise PSF model and the residual of best
matched tinytim PSF subtraction has a average relative fraction of
original image of 2 - 4 % level. For the fit routine I used this
time, I simply removed the 'super residual' model from the original
image and carry out the fit. The flux of A and B purely came from the
amplitude of the two components of the PSF. I did not count any flux
from the residual model into the flux of A or B.

An average relative fraction of 2-4% of the residual model could be a
potential source of uncertainty. Especially for the case that I
ignored the flux from the residual at all. However, I have not come up
with any idea on including the residual flux to the final result. I
think we need further discussion about this point.

>a) When you say you carried out a "two component tinytim PSF fit", it is not clear to me what you mean.  I assume the linear superposition of two TinyTim PSFs.  But do you mean one for A and one for B that are otherwise identical (or perhaps different in some manner other than brightness?).  Or do you mean for B (and perhaps also A) you have used a combination  of TinyTim PSFs that, in combination (perhaps with different defocus of color terms?) better represent the observed PSF?        

I used different PSFs for A and B. My fitting routine firstly
generates a list of PSFs using the position of A and the NIR spectrum
of A that comes from Bonnefoy et. al. 2014 with different telescope
jittering. I fit this PSF with an area where the image of B is mostly
excluded ( using a mask of 3-pixel radius centered on B) to the image
of A to find the best matched position and Jittering. Next, I use this
jittering to generate a PSF of B with B's position on detector and B's
spectrum that comes from Patience et al. 2010. In the third step, I
fit the two PSFs together with the position of A fixed , and to find
the best matched position of B and amplitudes of 2 PSFs.

>b) To me it is interesting (but not really unexpected) that binning
>by "same position angle" (i.e., spacecraft roll angle) improves.
>Off-rolling does thermally destablise the PSF to some extent - by
>changing the angle to the sub-solar point on the Earth as the
>telescope orbits and can drive quasi-breathing modes.  I am a bit
>surprised that these stabilize out as well as they seem to do (as
>exhibited by the factor of 10 improvement in chisq).  It would be
>interesting to know how much of that improvement is do to "same
>dither position" and how much to "same roll" (as differently binned).
>I am sure they both play together to reduce the residuals, but
>knowing this could have influence on how future observations might be
>constructed.

The position depandency of the residual pattern comes from at least
three parts.

1. Tinytim does not model the reflection light well and it has a
position depandency.
2. The imperfection of flat field is not modeled with TinyTim.
3. The PSFs are sampled differently at different position with a low
sample rate.

I would guess that the third point plays a key role in the difference
of residual pattern. Thus I think it difficult to tell 

> Overall, these look good; the question is, of course, how much of the
> apparent trend is real.  One note here: It is curious how both A and B
> have an increase in the first 3 orbits and then a different behavior
> in orbits 4-6.

>Could you explain how exactly do you determine the normalization
>factors for the different angles/dithering positions?

I median combined the fluxes calculated with images taking with same
filter, dithering position and roll angles, and devided the median
combination from every photometric result of these exposures. 

> Daniel asks: "how much of the apparent trend is real".  This might be
> difficult to ascertain.  Clearly the F125W and F160W for A seem well
> correlated (1st 3 vs last 3 orbits) , but that correlation possibly
> could still be instrumental.  If you took the new light curves as
> binned, for B:

> if you average all the points together in each orbit (loosing the
>  finer temporal information) is the change in normalized flux for B
>  over the six orbits also "consistent" from F125W to F160W **AND** is it
>  correlated with A?  It's a little harder to tell (quantitatively) as
>  plotted for B simply because it is noisier than A.  In both A and B
>  (both bands) the flux (by eye) also seems lower in the last three
>  orbits and MAYBE the is a small secular rise in orbits 1-3.  I would
>  expect that behavior in A and B to be independent, whereas if
>  correalted that may be an instrumental signature.

New plot needed. Plot the correlation of A and B with orbit combined points

> This looks quite nice and indeed, the 10.9 hours is not a period that
> I would obviously associate with an instrumental artifact.  Have you
> tried the same for the F160W LC? It would be a nice verification if
> you would get a similar periodicity.

By eye, light curve of F160W does not show a sine-wave like
shape. Thus I do not trust the result of a least square fit very
much. The least square fit results in a sine curve with a period of
9.26 hr. I also tried to fit the F160W light curve with a sine curve
that has a fixed period of 10.9 hr. I plotted the two best fit sine
curves together with the original observation.



> Also, to be consistent, can you please use the same fitting procedure
> for A (in both filters) and send similar plots?

I did the fitting for A in both fittings. The rise in first three
orbits is the main feature that defines the sin wave in the
fit. However if it were truly part of a sin wave, the sine function is
not well constrained by this small segment. For the light curve of
F125W, the fitting routine found a best fitted curve with a period of
6.86 hr. However the points in the 5th orbit are totally off the
fitted curve. For F160W, the fitting routine failed to converge when
fitting a sine curve to the light curve.


> (c) I assume the 10.9 hour fit came from a least-squares analysis --
> not quite a full observing/sampling period.  "By eye" it certainly
> loooks good, but might be interesting to also do a simple periodogram
> analysis, just to see if this might be an alias?

I thought about this idea before. However, 10.9 hour is longer than the
observation baseline and we if that were the case, we did not have a
periodical signal. I was wondering whether the periodogram would work
for data that does not cover a whole period.

