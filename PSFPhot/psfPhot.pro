
;;;;;generating PSfs;;;;;;;;;;;;

PRO makePSF, infn, normAper = normAper
  IF N_elements(normAper) EQ 0 THEN normAper = 5
  restore, infn
  filter = [0, 1]
  rollAngle = [101, 129]
  FOR i = 0, 1 DO BEGIN
     IF i EQ 0 THEN flt = 'F125W' ELSE flt = 'F160W'
     FOR j = 0, 1 DO BEGIN
        IF j EQ 0 THEN cen=[109., 166.] ELSE cen = [126., 171.]
        idList = where((infoList1.filter EQ infoList1[filter[i]].filter) AND infoList1.rollAngle EQ rollAngle[j])
        images = cube1[*, *, idList]
        psf = buildPSF(images, normAper, cen)
        saveFn = flt + strn(rollAngle[j]) + '.sav'
        save, psf, file = saveFn
     ENDFOR
  ENDFOR
END

FUNCTION buildPSF, images, normAper, cen
  imsSz = size(images)
  nIms = imsSz[imsSz[0]]
  psf = fltarr(imsSz[1], imsSz[2])
  FOR i = 0, nIms - 1 DO psf = psf + images[*, *, i]
  psfcen = findpeak(psf, cen[0], cen[1])
  aper, psf, psfcen[0], psfcen[1], f, ef, s, es, 1, 5.0, [10, 15], [-1e10, 1e10], /flux
  sky, psf, skymode, skysig
  return, (psf - skymode)/f[0]
END


FUNCTION findPeak, im, x0, y0, range=range
  IF N_ELEMENTS(range) EQ 0 THEN range = 10
  xlow = floor(x0 - range)
  ylow = floor(y0 - range)
  yfit = mpfit2dpeak(im[xlow:xlow + 2*range, ylow:ylow+2*range], params, /moffat)
  return, [params[4] + xlow, params[5] + ylow]
END

;;;;;;fit PSF;;;;;;

FUNCTION fitPSF, im, psfim, cen, fitSize, expoTime, skysig
  COMMON PSFsurf, psf
  cood = findPeak(im, cen[0], cen[1])
  immasked = im[floor(cood[0]) - fitSize:floor(cood[0]) + fitSize + 1, floor(cood[1]) - fitSize:floor(cood[1]) + fitSize + 1] * expoTime
  sigma = sqrt(abs(immasked) + (expoTime *skysig)^2)
  psf = psfim[floor(cood[0]) - fitSize:floor(cood[0]) + fitSize + 1, floor(cood[1]) - fitSize:floor(cood[1]) + fitSize + 1]
  PSFsz = size(psf)
  meshgrid, findgen(PSFsz[1]), findgen(PSFsz[2]), xx, yy
  fitParams = MPFIT2dFUN('PSFfunc', xx, yy, immasked, sigma, [8700 * expoTime, 0])
  flux = fitParams[0]/expoTime
  stop
  return, flux
END

FUNCTION PSFfunc, x, y, params
  COMMON PSFsurf, psf
  zmod = psf[x, y] * params[0] + params[1]
  return, zmod
END

  





  