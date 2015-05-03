;+
; NAME:
;
;
;
; PURPOSE:
;
;
;
; CATEGORY:
;
;
;
; CALLING SEQUENCE:
;
;
;
; INPUTS:
;
;
;
; OPTIONAL INPUTS:
;
;
;
; KEYWORD PARAMETERS:
;
;
;
; OUTPUTS:
;
;
;
; OPTIONAL OUTPUTS:
;
;
;
; COMMON BLOCKS:
;
;
;
; SIDE EFFECTS:
;
;
;
; RESTRICTIONS:
;
;
;
; PROCEDURE:
;
;
;
; EXAMPLE:
;
;
;
; MODIFICATION HISTORY:
;
;-

FUNCTION filename
  time = systime()
  mm = strmid(time, 4, 3)
  dd = string(uint(strmid(time, 8, 2)), format = '(I2.2)')
  year = strmid(time, 20, 4)
  fn = year + '_' + mm + '_' + dd
  return, fn
END

FUNCTION maskoutdq, dq, flagList=flaglist
  ;; make bad pixel mask using dq array.
  ;; according to some papers, flag 8, 32, 512 could cause seriour
  ;; problem for photometry
  ;; the pixel that has these flags will be assigned a mask value 0,
  ;; good pixel will be assigned mask value 1
  IF N_elements(flagList) EQ 0 THEN flagList = [8, 32, 512]
  dq = long(dq)
  mask = dq-dq+1 ;;initialize mask
  FOR k=0, n_elements(flagList) - 1 DO BEGIN
     mask = mask * (1- dq/flagList[k] MOD 2)
  ENDFOR 
  return, mask
END

FUNCTION prepData, infoStruct, dataDir, im125, im160, fix_bad = fix_bad
  ;; apply no shift to the image
  ;; process F125 and F160 individually
  IF n_elements(fix_bad) EQ 0 THEN fix_bad = 0 ELSE fix_bad = 1
  F125ID = where(infoStruct.filter EQ 'F125W')
  F160ID = where(infoStruct.filter EQ 'F160W')

  nFile = N_ELEMENTS(infoStruct.filename)
  xoff = fltarr(nFile)
  yoff = fltarr(nFile)
  cube = MAKE_ARRAY(256, 256, nFile, /DOUBLE) ;; list to save images
  errorCube = MAKE_ARRAY(256, 256, nFile, /Double) ;; save the err array
  dqMaskCube = MAKE_ARRAY(256, 256, nFile, /Double) ;; save the datacube mask
  imageSz = 256
  FOR i = 0, nFile -1 DO BEGIN
     im = mrdfits(dataDir + infoStruct.filename[i], 1, header1,/silent)
     err = mrdfits(dataDir + infoStruct.filename[i], 2, errhd,/silent) ;; read the error array
     dq = mrdfits(dataDir + infoStruct.filename[i], 3, dqhd,/silent)
     dqMask = maskoutdq(dq)
     fixpix, im, dqMask, im_fixed, /silent ;; use fixpix to fix the bad pixel for cross correlation
     
     IF infoStruct.filter[i] EQ 'F125W' THEN im0 = im125 ELSE im0 = im160
     corr = crosscorr(im0, im_fixed, pmax, dxy, range = 10) ;; use bad pixel fixed image for cross correlation
     
     xoff[i] = dxy[0]
     yoff[i] = dxy[1]
     IF fix_bad NE 0 THEN cube[*,*, i] = im_fixed ELSE cube[*, *, i] = im
     errorCube[*, *, i] = err
     dqMaskCube[*, *, i] = dqMask
     print,i,' image finished preparation'
  ENDFOR
  infoStruct = add_tag(infoStruct, 'xoff', xoff)
  infoStruct = add_tag(infoStruct, 'yoff', yoff)
  saveFN = filename() + '_prepared.sav'
  save, cube, errorCube, dqMaskCube, infoStruct, filename = saveFN
  return, saveFn
END


FUNCTION prepImaData, infoStruct, dataDir
  F125ID = where(infoStruct.filter EQ 'F125W')
  F160ID = where(infoStruct.filter EQ 'F160W')
  F125SubRd = [1, 6, 11, 16]
  F160SubRd = [1, 6]
  ;; read the first images for two filters, as the reference images
  im125 = readImaFile(dataDir + infoStruct.filename[F125ID[0]], F125SubRd)
  im160 = readImaFile(dataDir + infoStruct.filename[F160ID[0]], F160SubRd)
  
  nFile = N_ELEMENTS(infoStruct.filename)
  xoff = fltarr(nFile)
  yoff = fltarr(nFile)
  cube = MAKE_ARRAY(266, 266, nFile, /DOUBLE) ;; list to save images
  imageSz = 266
  FOR i = 0, nFile -1 DO BEGIN
     IF infoStruct.filter[i] EQ 'F125W' THEN BEGIN
        im0 = im125
        im = readImaFile(dataDir + infoStruct.filename[i], F125SubRd)
     ENDIF ELSE BEGIN
        im0 = im160
        im = readImaFile(dataDir + infoStruct.filename[i], F160SubRd)
     ENDELSE 
     corr = crosscorr(im0, im, pmax, dxy, range = 10)
     xoff[i] = dxy[0]
     yoff[i] = dxy[1]
     cube[*,*, i] = im
     print,'i',' image finished preparation'
  ENDFOR
  infoStruct = add_tag(infoStruct, 'xoff', xoff)
  infoStruct = add_tag(infoStruct, 'yoff', yoff)
  saveFN = filename() + '_prepared.sav'
  save, cube, infoStruct, filename = saveFN
  return, saveFn
END

FUNCTION readImaFile, filename, subReadID
  ;; function to read IMA file
  ;; average combine subreads
  im = fltarr(266, 266)
  FOR i = 0, N_ELEMENTS(subReadID) - 1 DO im = im + mrdfits(filename, subReadID[i])
  return, im/N_elements(subReadID)
END


FUNCTION findPeak, im, x0, y0, range=range
  ;; use Gaussian profile to fit the image to find the center of the
  ;; unsaturated image
  IF N_ELEMENTS(range) EQ 0 THEN range = 10
  xlow = floor(x0 - range)
  ylow = floor(y0 - range)
  yfit = mpfit2dpeak(im[xlow:xlow + 2*range, ylow:ylow+2*range], params)
  return, [params[4] + xlow, params[5] + ylow]
END
FUNCTION shiftMask, mask, dx, dy
  invMask = fshift(1-mask, dx, dy)
  invMask[where(invMask NE 0)] = 1 ;; pixel contaminated by hot pixel during shift is masked out.
  return, 1-invMask
END

FUNCTION searchPSF, id0, satisfyID, aperRadius, preSelectPSF = preSelectPSF
  ;; deal with the unaligned prepared images
  COMMON preparedData, cube, dqCube, errCube, infoList, nImages, xMesh, yMesh
  IF keyword_set(preselectPSF) EQ 0 THEN preSelectPSF = 0 
  ;; decide whether do pre-selection for PSF. IF do, onlyuse the PSF
  ;; images that have small fractional displacement to the original
  ;; image
  
  imSize = (size(cube))[1]                            ;; ima file is 266*266
  primaryCen = [114.212, 169.284] + (imSize - 256)/2. ;; center of the primary star on the reference image (the very first image)
  primaryCen = primaryCen + [infoList.xoff[id0], infoList.yoff[id0]] ;; and apply the displacement
  
  dx = infoList.xoff[satisfyID] - infoList.xoff[id0]
  dy = infoList.yoff[satisfyID] - infoList.yoff[id0]
  IF preSelectPSF NE 0 THEN BEGIN 
     d2Int = (dx - round(dx))^2 + (dy - round(dy))^2 ;; fractional part of the shift
     ID_i = (where(d2Int EQ min(d2Int)))[0:preSelectPSF]     
     PSF_id = satisfyID[ID_i] ;; choose the satisfied PSF that has the smallest fractional pixel shift so that PSF change is the smallest
  ENDIF ELSE BEGIN
     PSF_id = satisfyID
  ENDELSE 

  secCen1 = [95., 209.] + (imSize - 256)/2.  ;; approximate center of the secondary star
  secCen2 = [130., 223.] + (imSize - 256)/2. ;; same as above, for different roll angle
  ;; precise measurement depend on a gaussian fitting
  image0 = cube[*, *, id0]
  
  IF infoList.posang[id0] LE 110 THEN BEGIN ;; Gaussian fitting for secondary center
     x0 = secCen1[0] + (infoList.dither[id0] MOD 2) * 10.2
     y0 = secCen1[1] + (infoList.dither[id0]/2) * 10.2
     secCen = findPeak(image0, x0, y0, range = 5) 
  ENDIF ELSE BEGIN
     x0 = secCen2[0] + (infoList.dither[id0] MOD 2) * 10.2
     y0 = secCen2[1] + (infoList.dither[id0]/2) * 10.2
     secCen = findPeak(image0, x0, y0, range = 5)
  ENDELSE
  coeffList = fltarr(N_elements(PSF_id))
  chisqList = fltarr(N_elements(PSF_id))
  
  meshgrid, (size(image0))[1], (size(image0))[2], xx, yy ;; prepare a grid for later use
  dist = sqrt((xx-secCen[0])^2 + (yy-secCen[1])^2)       ;; define region of interest
  ROI = where(dist LE aperRadius)
  FOR i=0, N_elements(PSF_id) -1 DO BEGIN 
     ;; disSecondary = sqrt((xMesh - secCen[0])^2 + (yMesh - secCen[1])^2)
     ;; annulusPri = where((disPrimary GE 30) AND (disPrimary LE 60))
     ;; annulusSec = where(disSecondary LE 15)
     ;; annulusEff = cgsetdifference(annulusPri, annulusSec)

     ;; locate the center of he secondary in PSF images
     mask_i = shiftMask(dqCube[*,*,PSF_id[i]], -dx[i], -dy[i])
     ;;; make sure that for PSF images, there are no bad pixels that
     ;;; are subtracted from the region of interest
     IF (where(mask_i[ROI] EQ 0))[0] NE -1 THEN BEGIN
        coeffList[i] = !Values.F_NAN
        chisqList[i] = !Values.F_NAN
        CONTINUE
     ENDIF
     
     image_i = fshift(cube[*, *, PSF_id[i]], -dx[i], -dy[i])

     IF infoList.posang[PSF_id[i]] le 110 THEN BEGIN
        x0 = secCen1[0] + (infoList.dither[PSF_id[i]] MOD 2) * 10.2 -dx[i]
        y0 = secCen1[1] + (infoList.dither[PSF_id[i]]/2) * 10.2 - dy[i]
        secCen_i = findPeak(image_i, x0, y0, range = 5) 
     ENDIF ELSE BEGIN
        x0 = secCen2[0] + (infoList.dither[PSF_id[i]] MOD 2) * 10.2 - dx[i]
        y0 = secCen2[1] + (infoList.dither[PSF_id[i]]/2) * 10.2 - dy[i]
        secCen_i = findPeak(image_i, x0, y0, range = 5)
     ENDELSE
     
     ;; mask out bad pixels and 
     mask = make_mask(dqCube[*, *, id0] * mask_i, [[primaryCen[0], primaryCen[1], 0, 30], [primaryCen[0], primaryCen[1], 60, 500], [secCen[0], secCen[1], 0, 10], [secCen_i[0], secCen_i[1], 0, 10]])
     mask = float(mask)/total(mask) ;; normalize the mask
     coeffList[i] = total(mask*image_i*image0)/total(mask*image_i*image_i);; simple calculation just by calculate the matrix
     chisqList[i] = total(mask * (image0 - coeffList[i]*image_i)^2)
  ENDFOR
  min_id = (where(chisqList EQ min(chisqList, /nan)))[0]
  psf_id0 = PSF_id[min_id]
  amp = coeffList[min_id]

  mask_psf = shiftMask(dqCube[*,*,psf_id0], -dx[min_id], -dy[min_id])
  ;; re-calculate the mask for PSF image
  
  mask = make_mask(dqCube[*, *, id0] * mask_i, [[primaryCen[0], primaryCen[1], 0, 30], [primaryCen[0], primaryCen[1], 60, 500], [secCen[0], secCen[1], 0, 10], [secCen_i[0], secCen_i[1], 0, 10]])
  skyImage = cube[*, *, id0] - amp*fshift(cube[*, *, psf_id0], -dx[min_id], -dy[min_id])
  skyImage[where(mask EQ 0)] = !VALUES.F_NAN ;; use mask to set the image in the mask to NaN
  sky, skyImage, skylevel, skysig, /nan
  return, [psf_id0, amp, skyLevel, skysig, secCen[0], secCen[1], dx[min_id], dy[min_id]] ; return psf id and c0
END


FUNCTION psf_subtraction, input_fn, aperRadius, Subtract
  COMMON preparedData, cube, dqMaskCube, errorCube, infoStruct, nImages, xMesh, yMesh
  restore, input_fn ;; restore data from data preparation PROCEDURE
  ;;restore, PSF_fn
  cube1 = cube
  szCube = size(cube)
  nImages = szCube[3]
  meshgrid, findgen(256), findgen(256), xMesh, yMesh
  skyLevel = fltarr(nImages)
  skySigma = fltarr(nImages)
  xCenter = fltarr(nImages)
  yCenter = fltarr(nImages)
  PSF_id = fltarr(nImages)
  PSF_amplitude = fltarr(nImages)
  FOR i = 0, nImages - 1 DO BEGIN
     angle_i = infoStruct.posang[i]
     filter_i = infoStruct.filter[i]
     satisfyID = where((infoStruct.filter EQ filter_i) AND (infoStruct.posang NE angle_i))
     fitResult = searchPSF(i, satisfyID, aperRadius)
     PSF_id[i] = fitResult[0]
     PSF_amplitude[i] = fitResult[1]
     skyLevel[i] = fitResult[2]
     skySigma[i] = fitResult[3]
     xCenter[i] = fitResult[4]
     yCenter[i] = fitResult[5]
     IF Subtract NE 0 THEN BEGIN
        cube1[*, *, i] = cube[*, *, i] - fitResult[1] * fshift(cube[*, *, psf_id[i]], -fitResult[6], -fitResult[7])
        errorCube[*, *, i] = sqrt(errorCube[*, *, i]^2 + (PSF_amplitude[i]*errorCube[*, *, psf_id[i]])^2) ;; modify the errorCube corrodinately
     ENDIF ELSE BEGIN
        cube1[*,*,i] = cube[*,*,i]
     ENDELSE
     
     print, i, ' image finished psf subtraction'
  ENDFOR
  infoStruct1 = add_tag(infoStruct, 'xCenter', xCenter)
  infoStruct1 = add_tag(infoStruct1, 'yCenter', yCenter)
  infoStruct1 = add_tag(infoStruct1, 'PSF_id', PSF_id)
  infoStruct1 = add_tag(infoStruct1, 'PSF_amplitute', PSF_amplitude)
  infoStruct1 = add_tag(infoStruct1, 'sky_level', skyLevel)
  infoStruct1 = add_tag(infoStruct1, 'sky_sigma', skySigma)
  output_fn = filename() + '_subtracted.sav'
  save, cube1, errorCube, dqMaskCube, infoStruct1, filename = output_fn
  return, output_fn
END

FUNCTION aperturePhot, inFn, aperRadius, include_bad
  restore, inFn
  szCube = size(cube1)
  nImages = szCube[3]
  flux = fltarr(nImages)
  fluxErr = fltarr(nImages)
  contaminated = fltarr(nImages)
  xFWHM = fltarr(nImages)
  yFWHM = fltarr(nImages)
  f125id = where(infoStruct1.filter EQ 'F125W')
  f160id = where(infoStruct1.filter EQ 'F160W')
  aperList = [aperRadius]
  FOR i = 0, nImages - 1 DO BEGIN
     image = cube1[*, *, i]

     expoTime = infoStruct1.exposure_time[i]
     ;; IF infoList1[f125id[i]].rollAngle EQ 101 THEN $
     ;;    gcntrd, image, 109., 166., xSec, ySec, 2.0 $ ;; search
                ;;    secondary center
     x0 = infoStruct1.xCenter[i]
     y0 = infoStruct1.yCenter[i]
     range = 10
     xlow = floor(x0 - range)
     ylow = floor(y0 - range)
     imageFit = mpfit2dpeak(image[xlow:xlow + 2*range, ylow:ylow+2*range], params)
     infoStruct1.xCenter[i] = xlow + params[4]
     infoStruct1.yCenter[i] = ylow + params[5]
     xFWHM[i] = 2.3548 * params[2]
     yFWHM[i] = 2.3548 * params[3]
     aper, image * expoTime, infoStruct1.xCenter[i], infoStruct1.yCenter[i], f, ef, sky, skyerr, $
           1, aperList, [30, 50], [-100, 1e7], /flux, $
           setskyval = [infoStruct1.sky_level[i] * expoTime, infoStruct1.sky_sigma[i] * expoTime, 7000],/silent,/nan
     flux[i] = f[0]/expoTime
     ;;fluxErr[i] = ef[0]/expoTime
     ;; calculate error using error Array
     meshgrid, 256, 256, xx, yy
     dist = sqrt((xx - infoStruct1.xCenter[i])^2 + (yy - infoStruct1.yCenter[i])^2)
     effID = where(dist LE aperRadius)
     fluxErr[i] = sqrt(total(((errorCube[*, *, i])[effID])^2 + infoStruct1.sky_sigma[i]))
     IF (where((dqMaskCube[*, *, i])[effID] EQ 0))[0] NE -1 THEN contaminated[i] = 1
     print, i, ' image finished photometry'
  ENDFOR
  infoStruct1 = add_tag(infoStruct1, 'flux', flux)
  infoStruct1 = add_tag(infoStruct1, 'fluxerr', fluxerr)
  infoStruct1 = add_tag(infoStruct1, 'xFWHM', xFWHM)
  infoStruct1 = add_tag(infoStruct1, 'yFWHM', yFWHM)
  infoStruct1 = add_tag(infoStruct1, 'contaminated', contaminated)
  output_fn =  filename() + '_aperPhot.sav'
  save, infoStruct1, file = output_fn
  return, output_fn
END


PRO aperturePhotPipeLine2, infoFile, fileType, aperRadius  = aperRadius, subtract = Subtract, fix_bad = fix_bad
  fileInfo = myReadCSV(infoFile, ['filename', 'filter', 'orbit', 'posang', 'dither', 'exposure_set','obs_date','obs_time','exposure_time'])
  IF N_elements(Subtract) EQ 0 THEN subtract = 1
;; if subtract = 1, subtract PSF image, else don't, default is subtract
  IF N_elements(fix_bad) EQ 0 THEN fix_bad = 0 ELSE fix_bad = 1
  ;; whether fix the bad pixel in photometry if fix_bad == 1, fix bad
  ;; pixel by interpolation over neighbor pixel using fix_bad routine,
  ;; default is not fit
  ;; However, when registering image using cross-correlation, the bad
  ;; pixels are always fixed.

  

  ;; read the first images for two filters, as the reference images
  im1250 = mrdfits('../data/ABPIC-B/icdg07p3q_flt.fits', 1, hd)
  dq1250 = mrdfits('../data/ABPIC-B/icdg07pcq_flt.fits', 3, hd)
  dqMask1250 = maskoutdq(dq1250)
  fixpix, im1250, dqMask1250, im125
  im1600 = mrdfits('../data/ABPIC-B/icdg07p7q_flt.fits', 1, hd) ;; define cross correlation reference image
  dq1600 = mrdfits('../data/ABPIC-B/icdg07p7q_flt.fits', 3, hd)
  dqMask1600 = maskoutdq(dq1600)
  fixpix, im1600, dqMask1600, im160
  IF n_elements(aperRadius) EQ 0 THEN aperRadius = 3
  
  IF fileType EQ 'flt' THEN BEGIN
     IF fix_bad THEN preparedFN = prepData(fileInfo, dataDir, im125, im160, /fix_bad) $
     ELSE preparedFN = prepData(fileInfo, dataDir, im125, im160)
     PSF_fn = 'flt_PSF.sav'
  ENDIF ELSE IF fileType EQ 'ima' THEN BEGIN
     IF fix_bad THEN preparedFN = prepData(fileInfo, dataDir, im125, im160, /fix_bad) $
     ELSE preparedFN = prepData(fileInfo, dataDir, im125, im160)

     PSF_fn = 'ima_PSF.sav'
  ENDIF ELSE IF (fileType EQ 'myfits')  THEN BEGIN
     IF fix_bad THEN preparedFN = prepData(fileInfo, dataDir, im125, im160, /fix_bad) $
     ELSE preparedFN = prepData(fileInfo, dataDir, im125, im160)

     PSF_fn = 'myfits_PSF.sav'
  ENDIF ELSE IF (fileType EQ 'noramp') THEN BEGIN
     dataDir = '../data/ABPIC-B_noramp/' ;; changable
     IF fix_bad THEN preparedFN = prepData(fileInfo, dataDir, im125, im160, /fix_bad) $
     ELSE preparedFN = prepData(fileInfo, dataDir, im125, im160)
  ENDIF ELSE IF (fileType EQ 'newflat') THEN BEGIN
     dataDir = '../data/ABPIC-B_noramp_newflat/' ;; changable
     IF fix_bad THEN preparedFN = prepData(fileInfo, dataDir, im125, im160, /fix_bad) $
     ELSE preparedFN = prepData(fileInfo, dataDir, im125, im160)
  ENDIF 
  subtractedFN = psf_subtraction(preparedFN, aperRadius, subtract)

  resultFN = aperturePhot(subtractedFN, aperRadius)
  resultCSVFN = filename() + '_' + fileType + '_aper=' + strn(aperRadius, length = 4) + '_result.csv'
  spawn, 'python sav2csv.py ' + resultFN + ' ' + resultCSVFN ;; convert .sav file to csv file for easier using.
END

