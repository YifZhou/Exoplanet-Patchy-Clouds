PRO subtract, im, center1, center2, subim1, subim2, nSamp = nSamp
  IF N_ELEMENTS(nSamp) EQ 0 THEN nSamp = 10
  c1 = findpeak(im, center1[0], center1[1], range = 5)
  c2 = findpeak(im, center2[0], center2[1], range = 5)
  c1 = floor(c1)
  c2 = floor(c2)
  subIm1 = im[c1[0]-20:c1[0]+20, c1[1]-20:c1[1]+20]
  subIm2 = im[c2[0]-20:c2[0]+20, c2[1]-20:c2[1]+20]
  ;; interpolation
  subim1 = congrid(subIm1, 41*nSamp, 41*nSamp, cubic = -0.5, /MINUS_ONE)
  subim2 = congrid(subIm2, 41*nSamp, 41*nSamp, cubic = -0.5, /MINUS_ONE)
  c1 = findpeak(subim1, 41*nSamp/2, 41*nSamp/2, range = 5*nSamp)
  c2 = findpeak(subim2, 41*nSamp/2, 41*nSamp/2, range = 5*nSamp)
  dc = c2 - c1
  subim2 = fshift(subim2, -dc[0], -dc[1])
  c2 = findpeak(subim2, 41*nSamp/2, 41*nSamp/2, range = 5*nSamp)
  print, c1
  subim2 = subim2 * c1[2]/c2[2]
  c2 = findpeak(subim2, 41*nSamp/2, 41*nSamp/2, range = 5*nSamp)
  print, c2
END

FUNCTION findPeak, im, x0, y0, range=range
  ;; use Gaussian profile to fit the image to find the center of the
  ;; unsaturated image
  IF N_ELEMENTS(range) EQ 0 THEN range = 10
  xlow = floor(x0 - range)
  ylow = floor(y0 - range)
  yfit = mpfit2dpeak(im[xlow:xlow + 2*range, ylow:ylow+2*range], params)
  print, params
  return, [params[4] + xlow, params[5] + ylow, params[1]]
END
