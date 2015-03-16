
;;;;;generating PSfs;;;;;;;;;;;;

;; FUNCTION makePSF, infn, filter, rollAngle, normAper = normAper
;;   IF N_elements(normAper) EQ 0 THEN normAper = 5
;;   restore, infn
;;   cen0 = [109, 166]
;;   cen1 = [126, 171]
;;   idList = where((infoList1.filter EQ infoList1[filter].filter) AND (infoList1.rollAngle EQ rollAngle))
;;   PSF = fltarr(256, 256)
;;   FOR i = 0, N_ELEMENTS(idList) - 1 DO BEGIN
;;      IF infoList1[idList[i]].rollAngle EQ 101 THEN cenxy = findPeak(cube1[*, *, idList[i]], cen0[0], cen0[1]) $
;;         ELSE cenxy = findPeak(cube1[*, *, idList[i]], cen1[0], cen1[1])
;;      oversamp = 20
;;      im_resample = congrid(cube1[*, *, idList[i]], 256*oversamp, 256*oversamp, cubic = -0.5)
;;      print, i
;;      im_shifted = fshift(im_resample, oversamp * (127 - cenxy[0]), oversamp * (127 - cenxy[1]))
;;      PSF = PSF + congrid(im_shifted, 256, 256, cubic = -0.5)
;;   ENDFOR
;;   skylevel = total(infoList1[idList].skylevel)
;;   skysigma = sqrt(total(infoList1[idList].skysigma^2))
;;   aper, psf, 127, 127, f, ef, s, es, 1, 5.0, [10, 15], [-1e10, 1e10], setskyval = [skylevel, skysigma, 7000], /flux
;;   return, (psf - skylevel)/ f[0]
;; END


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
        skylevel = total(infoList1[idList].skylevel)
        skysig = sqrt(total(infoList1[idList].skysigma^2))
        psf = buildPSF(images, normAper, cen, skylevel, skysig)
        saveFn = flt + strn(rollAngle[j]) + '.sav'
        save, psf, file = saveFn
     ENDFOR
  ENDFOR
END

FUNCTION buildPSF, images, normAper, cen, skylevel, skysig
  imsSz = size(images)
  nIms = imsSz[imsSz[0]]
  psf = fltarr(imsSz[1], imsSz[2])
  FOR i = 0, nIms - 1 DO psf = psf + images[*, *, i]
  psfcen = findpeak(psf, cen[0], cen[1])
  aper, psf, psfcen[0], psfcen[1], f, ef, s, es, 1, 5.0, [10, 15], [-1e10, 1e10], setskyval = [skylevel, skysig, 7000], /flux
  return, (psf - skylevel)/f[0]
END


FUNCTION findPeak, im, x0, y0, range=range
  IF N_ELEMENTS(range) EQ 0 THEN range = 10
  xlow = floor(x0 - range)
  ylow = floor(y0 - range)
  yfit = mpfit2dpeak(im[xlow:xlow + 2*range, ylow:ylow+2*range], params, /moffat)
  return, [params[4] + xlow, params[5] + ylow]
END

FUNCTION mychisq, im, psf, sigma, params
  return, total((im - psf * params[0] - params[1])^2/sigma^2)
END

;;;;;;fit PSF;;;;;;

FUNCTION fitPSF, im, psfim, cen, fitSize, expoTime, skysig, oversample = oversample
  COMMON PSFsurf, psf
  IF N_ELEMENTS(oversample) EQ 0 THEN oversample = 10
  cood = findPeak(im, cen[0], cen[1])
  immasked = im[floor(cood[0]) - fitSize:floor(cood[0]) + fitSize + 1, floor(cood[1]) - fitSize:floor(cood[1]) + fitSize + 1] * expoTime
  psf = psfim[floor(cood[0]) - fitSize:floor(cood[0]) + fitSize + 1, floor(cood[1]) - fitSize:floor(cood[1]) + fitSize + 1]
  PSFsz = size(psf)
  immasked = congrid(immasked, PSFsz[1] * oversample, PSFsz[2] * oversample, cubic = -0.5)
  sigma = sqrt(abs(immasked) + (expoTime *skysig)^2)
  psf = congrid(psf, PSFsz[1] * oversample, PSFsz[2] * oversample, cubic = -0.5)
  PSFsz = size(psf)
  meshgrid, findgen(PSFsz[1]), findgen(PSFsz[2]), xx, yy
  fitParams = MPFIT2dFUN('PSFfunc', xx, yy, immasked, sigma, [8000 * expoTime, 0])
  flux = fitParams[0]/expoTime
  chisq = mychisq(immasked, psf, sigma, fitparams)
  return, [flux, chisq]
END

FUNCTION PSFfunc, x, y, params
  COMMON PSFsurf, psf
  zmod = psf[x, y] * params[0] + params[1]
  return, zmod
END

PRO PSFphot, infn, PSFfn, outfn
  restore, infn
  restore, PSFfn
  cen1 =[109., 166.]
  cen2 = [126., 171.]
  F125List = where(infoList1.filter EQ infoList1[0].filter)
  F160List = where(infoList1.filter EQ infoList1[1].filter)
  F125Flux = fltarr(N_ELEMENTS(F125List))
  F160Flux = fltarr(N_elements(F160List))
  f125chisq = fltarr(N_elements(F125List))
  f160chisq = fltarr(N_elements(F160List))

  FOR i = 0, N_elements(F125List) - 1 DO BEGIN
     IF infoList1[F125List[i]].rollAngle EQ 101 THEN BEGIN
        cen = cen1
        PSF = PSF0[*,*,0]
     ENDIF ELSE BEGIN
        cen = cen2
        PSF = PSF0[*,*,1]
     ENDELSE
     f= fitPSF(cube1[*,*,F125List[i]], PSF, cen, 8, infoList1[F125List[i]].exposureTime, infoList1[F125List[i]].skysigma)
     F125Flux[i] = f[0]
     f125chisq[i] = f[1]
  ENDFOR
  
  FOR i = 0, N_elements(F160List) - 1 DO BEGIN
     IF infoList1[F160List[i]].rollAngle EQ 101 THEN BEGIN
        cen = cen1
        PSF = PSF0[*,*,2]
     ENDIF ELSE BEGIN
        cen = cen2
        PSF = PSF0[*,*,3]
     ENDELSE
     f = fitPSF(cube1[*,*,F160List[i]], PSF, cen, 8, infoList1[F160List[i]].exposureTime, infoList1[F160List[i]].skysigma)
     F160Flux[i] = f[0]
     f160chisq[i] = f[1]

  ENDFOR
stop
END 
  





  
