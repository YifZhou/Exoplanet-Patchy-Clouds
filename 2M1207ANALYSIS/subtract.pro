PRO subtract, im, center1, center2, subim1, subim2, maskVar, nSamp = nSamp
  IF N_ELEMENTS(nSamp) EQ 0 THEN nSamp = 10
  c1 = findpeak(im, center1[0], center1[1], range = 5)
  c2 = findpeak(im, center2[0], center2[1], range = 5)
  c1 = floor(c1)
  c2 = floor(c2)
  subIm1 = im[c1[0]-20:c1[0]+19, c1[1]-20:c1[1]+19]
  subIm2 = im[c2[0]-20:c2[0]+19, c2[1]-20:c2[1]+19]
  mask = make_mask(fltarr(256, 256) + 1, maskVar)
  subMask = mask[c1[0]-20:c1[0]+19, c1[1]-20:c1[1]+19]
  ;; interpolation
  subim1_int = congrid(subIm1, 40*nSamp, 40*nSamp, cubic = -0.5, /MINUS_ONE)
  subim2_int = congrid(subIm2, 40*nSamp, 40*nSamp, cubic = -0.5, /MINUS_ONE)
  subMask = congrid(subMask, 40*nSamp, 40*nSamp, /minus_one)
  c1 = findpeak(subim1, 40*nSamp/2, 40*nSamp/2, range = 3*nSamp)
  c2 = findpeak(subim2, 40*nSamp/2, 40*nSamp/2, range = 3*nSamp)
  corr = crosscorr(subim1, subim2 * c1[2]/c2[2], pmax, dxy, range = 5)
  dxy3 = normxcorr2(subim1, subim2, weight=submask)
  dc = c2 - c1
  print, dxy/10
  print, dc
  print, dxy3/10
  print, c1
  print, c2
;  subim2 = fshift(subim2, -dxy[0], -dxy[1])
  ;; c2 = findpeak(subim2, 41*nSamp/2, 41*nSamp/2, range = 3*nSamp)
  ;; print, c1
  ;; subim2 = subim2 * c1[2]/c2[2]
  ;; c2 = findpeak(subim2, 41*nSamp/2, 41*nSamp/2, range = 3*nSamp)
  ;; print, c2
END

FUNCTION findPeak, im, x0, y0, range=range
  ;; use Gaussian profile to fit the image to find the center of the
  ;; unsaturated image
  IF N_ELEMENTS(range) EQ 0 THEN range = 10
  xlow = floor(x0 - range)
  ylow = floor(y0 - range)
  yfit = mpfit2dpeak(im[xlow:xlow + 2*range, ylow:ylow+2*range], params)
  return, [params[4] + xlow, params[5] + ylow, params[1]]
END
