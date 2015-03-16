;; use tinytim psf to do the photometry

PRO PSFPhotPipeLine2, subtractedFN, fileType, ROIRadius=ROIRadius
  IF N_elements(ROIRadius) EQ 0 THEN ROIRadius = 5
  resultFN = PSFPhot(subtractedFN, ROIRadius = ROIRadius)
  resultCSVFN = filename() + '_' + fileType + '_PSF_result.csv'
  spawn, 'python sav2csv.py ' + resultFN + ' ' + resultCSVFN ;; convert .sav file to csv file for easier using.
END

FUNCTION makePSF, fn, dx, dy
  im = mrdfits(fn)
  diffusion = [[0.0007, 0.025,  0.0007],$
               [0.0250, 0.897,  0.0250],$
               [0.0007, 0.025,  0.0007]]
  dx0 = dx
  dy0 = dy
  WHILE 1 DO BEGIN
  im1 = fshift(im[1:270, 1:270], dx*10, dy*10)
  im0 = convol(binPSF(im1), diffusion) ;;covolve with the diffusion kernel
  psffit = mpfit2dpeak(im0, params)
  ddx = params[4] - 13 - dx0
  ddy = params[5] - 13 - dy0
  IF (abs(ddx) LE 0.001) AND (abs(ddy) LE 0.001) THEN BEGIN
     BREAK
  ENDIF ELSE BEGIN
     dx = dx-ddx
     dy = dy-ddy
  ENDELSE 
  ENDWHILE
  return, im0/total(im0) ;;normalize the psf
END
FUNCTION binPSF,psf
  binned = fltarr(27, 27)
  FOR i=0,26 DO BEGIN
     FOR j=0,26 DO BEGIN
        binned[i, j] = total(psf[10*i:10*i + 9, 10*j : 10*j+9])
     ENDFOR
  ENDFOR
  return, binned
END

FUNCTION PSFPhot, inFn, ROIRadius=ROIRadius
  IF N_ELEMENTS(ROIRadius) EQ 0 THEN ROIRadius = 5.0
  restore, inFn
  szCube = size(cube1)
  nImages = szCube[3]
  flux = fltarr(nImages)
  fluxErr = fltarr(nImages)
  xFWHM = fltarr(nImages)
  yFWHM = fltarr(nImages)
  FOR i = 0, nImages - 1 DO BEGIN
     image = cube1[*, *, i]
     expoTime = infoStruct1.exposure_time[i]
     ;; IF infoList1[f125id[i]].rollAngle EQ 101 THEN $
     ;;    gcntrd, image, 109., 166., xSec, ySec, 2.0 $ ;; search
                ;;    secondary center
     x0 = infoStruct1.xCenter[i]
     y0 = infoStruct1.yCenter[i]
     range = 5
     xlow = floor(x0 - range)
     ylow = floor(y0 - range)
     imageFit = mpfit2dpeak(image[xlow:xlow + 2*range, ylow:ylow+2*range], params)
     infoStruct1.xCenter[i] = xlow + params[4]
     infoStruct1.yCenter[i] = ylow + params[5]
     xFWHM[i] = 2.3548 * params[2]
     yFWHM[i] = 2.3548 * params[3]
     IF infoStruct1.filter[i] EQ 'F125W' THEN BEGIN
        IF infoStruct1.posang[i] EQ 129.0 THEN psffn = 'F125W00.fits'$
        ELSE psffn = 'F125W01.fits'
     ENDIF ELSE BEGIN
        IF infoStruct1.posang[i] EQ 129.0 THEN psffn = 'F160W00.fits'$
        ELSE psffn = 'F160W01.fits'
     ENDELSE
     dx = infoStruct1.xCenter[i] - round(infoStruct1.xCenter[i])
     dy = infoStruct1.yCenter[i] - round(infoStruct1.yCenter[i])
     psf = makePSF(psffn, dx, dy)
     im_roi = image[round(infoStruct1.xCenter[i]) - ROIRadius: round(infoStruct1.xCenter[i]) + ROIRadius, round(infoStruct1.yCenter[i]) - ROIRadius: round(infoStruct1.yCenter[i]) + ROIRadius]*expoTime
     psf_roi = psf[13 -ROIRadius: 13+ROIRadius, 13 -ROIRadius: 13+ROIRadius]
     err_roi = sqrt(abs(im_roi) *expoTime)
     fit = fitPSF(im_roi, psf_roi, err_roi)
     flux[i] = fit[0]/expoTime
     print, fit[2]/N_ELEMENTS(psf_roi)
     meshgrid, 256, 256, xx, yy
     dist = sqrt((xx - infoStruct1.xCenter[i])^2 + (yy - infoStruct1.yCenter[i])^2)
     effID = where(dist LE ROIRadius)
     fluxErr[i] = sqrt(total(((sqrt(abs(image) /expoTime))[effID])^2))
     print, i, ' image finished photometry'
  ENDFOR
  infoStruct1 = add_tag(infoStruct1, 'flux', flux)
  infoStruct1 = add_tag(infoStruct1, 'fluxerr', fluxerr)
  infoStruct1 = add_tag(infoStruct1, 'xFWHM', xFWHM)
  infoStruct1 = add_tag(infoStruct1, 'yFWHM', yFWHM)
  output_fn =  filename() + '_PSFPhot.sav'
  save, infoStruct1, file = output_fn
  return, output_fn
END

FUNCTION fitPSF, im, psfim, err
  COMMON PSFsurf, psf
  psf = psfim
  PSFsz = size(psf)
  meshgrid, findgen(PSFsz[1]), findgen(PSFsz[2]), xx, yy
  fitParams = MPFIT2dFUN('PSFfunc', xx, yy, im, err, [10000, 0],/quiet)
  flux = fitParams[0]
  sky = fitParams[1]
  chisq = mychisq(im, psf, err, fitparams)
  return, [flux, sky, chisq]
END

FUNCTION PSFfunc, x, y, params
  COMMON PSFsurf, psf
  zmod = psf[x, y] * params[0] + params[1]
  return, zmod
END

FUNCTION mychisq, im, psf, sigma, params
  return, total((im - psf * params[0] - params[1])^2/sigma^2)
END

FUNCTION filename
  time = systime()
  mm = strmid(time, 4, 3)
  dd = string(uint(strmid(time, 8, 2)), format = '(I2.2)')
  year = strmid(time, 20, 4)
  fn = year + '_' + mm + '_' + dd
  return, fn
END
