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

PRO aperturePhotPipeLine, infoFile
  fileInfo = myReadCSV(infoFile, ['filename', 'filter', 'orbit', 'posang', 'dither', 'exposure_set','obs_date','obs_time','exposure_time'])
  dataDir = '../data/ABPIC-B/' ;; changable
  saveFN = prepData(fileInfo, dataDir)
END

FUNCTION myReadCSV,fn, tags
  strct = read_csv(fn)
  return, rename_tags(strct, ['FIELD1','FIELD2','FIELD3','FIELD4','FIELD5','FIELD6','FIELD7','FIELD8','FIELD9'], tags)
END

FUNCTION prepData, infoStruct, dataDir
  ;; apply no shift to the image
  F125ID = where(infoStruct.filter EQ 'F125W')
  F160ID = where(infoStruct.filter EQ 'F160W')
  im125 = mrdfits(dataDir + infoStruct.filename[F125ID[0]], 1, hd)
  im160 = mrdfits(dataDir + infoStruct.filename[F160ID[0]], 1, hd)
  nFile = N_ELEMENTS(infoStruct.filename)
  xoff = fltarr(nFile)
  yoff = fltarr(nFile)
  cube = MAKE_ARRAY(256, 256, nFile, /DOUBLE) ;; list to save images
  imageSz = 256
  FOR i = 0, nFile -1 DO BEGIN
     im = mrdfits(dataDir + infoStruct.filename[i], 1, header1)
     IF infoStruct.filter[i] EQ 'F125W' THEN im0 = im125 ELSE im0 = im160
     corr = crosscorr(im0, im, pmax, dxy, range = 10)
     xoff[i] = dxy[0]
     yoff[i] = dxy[1]
     cube[*,*, i] = im
     print,'i',' image prepared'
  ENDFOR
  infoStruct = add_tag(infoStruct, 'xoff', xoff)
  infoStruct = add_tag(infoStruct, 'yoff', yoff)
  saveFN = strn(floor(systime(/julian))) + '_prepared.sav'
  save, cube, infoStruct, filename = saveFN
  return, saveFn
END


FUNCTION findPeak, im, x0, y0, range=range
  IF N_ELEMENTS(range) EQ 0 THEN range = 10
  xlow = floor(x0 - range)
  ylow = floor(y0 - range)
  yfit = mpfit2dpeak(im[xlow:xlow + 2*range, ylow:ylow+2*range], params, /moffat)
  return, [params[4] + xlow, params[5] + ylow]
END

FUNCTION searchPSF, id0, satisfyID
  ;; deal with the unaligned prepared images
  COMMON preparedData, cube, infoList, nImages, xMesh, yMesh
  dx = infoList.xoff - infoList.xoff[id0]
  dy = infoList.yoff - infoList.yoff[id0]
  dx_frac = (abs(dx - round(dx)))[satisfyID]
  dy_frac = (abs(dy - round(dy)))[satisfyID]  ;; only consider satisfied
  satisfyID = satisfyID[(sort(dx_frac^2 + dy_frac^2))[0:4]] ;; choose PSF that has the smallest fractional shift
  nSatisfied = N_ELEMENTS(satisfyID)
  disPrimary = sqrt((xMesh - 127)^2 + (yMesh - 127)^2)
  secCen1 = [95., 209.]
  secCen2 = [130., 223.]
  image0 = cube[*, *, id0]
  IF infoList.posang[id0] LE 110 THEN BEGIN
     x0 = secCen1[0] + (infoList.dither[id0] MOD 2) * 10.2
     y0 = secCen1[1] + (infoList.dither[id0]/2) * 10.2
     secCen = findPeak(image0, x0, y0, range = 5) 
     ENDIF ELSE BEGIN
        x0 = secCen2[0] + (infoList.dither[id0] MOD 2) * 10.2
        y0 = secCen2[1] + (infoList.dither[id0]/2) * 10.2
        secCen = findPeak(image0, x0, y0, range = 5)
     ENDELSE
     
  disSecondary = sqrt((xMesh - secCen[0])^2 + (yMesh - secCen[1])^2)
  annulusPri = where((disPrimary GE 30) AND (disPrimary LE 60))
  annulusSec = where(disSecondary LE 15)
  annulusEff = cgsetdifference(annulusPri, annulusSec)
  c_fit = 0.99 + 0.002*findgen(11)
  c_int = congrid(c_fit, 200,/interp)
  residual = fltarr(n_elements(c_fit))
  cList = fltarr(nSatisfied)
  resList = fltarr(nSatisfied)
  skylevelList = fltarr(nSatisfied)
  skysigList = fltarr(nSatisfied)
  FOR i = 0, nSatisfied - 1  DO BEGIN
     id_i = satisfyID[i]
     image_i = fshift(cube[*, *, id_i], -dx[id_i], -dy[id_i])
     IF infoList.posang[id_i] le 110 THEN BEGIN
        x0 = secCen1[0] + (infoList.dither[id_i] MOD 2) * 10.2 -dx[id_i]
        y0 = secCen1[1] + (infoList.dither[id_i]/2) * 10.2 - dy[id_i]
        secCen_i = findPeak(image_i, x0, y0, range = 5) 
     ENDIF ELSE BEGIN
        x0 = secCen2[0] + (infoList.dither[id_i] MOD 2) * 10.2 - dx[id_i]
        y0 = secCen2[1] + (infoList.dither[id_i]/2) * 10.2 - dy[id_i]
        secCen_i = findPeak(image_i, x0, y0, range = 5)
     ENDELSE
     
     disRolled = sqrt((xMesh - SecCen_i[0])^2 + (yMesh - SecCen_i[1])^2)
     annulusRolled = where(disRolled LE 15)
     annulusEff_i0 = cgsetdifference(annulusEff, annulusRolled)
     sky, (image0 - image_i)[annulusEff_i0], mode, std, /silent
     annulusEff_i = annulusEff_i0[where(abs((image0 - image_i)[annulusEff_i0]) LE 3 *std)]
     print,n_elements(annulusEff_i0) - N_ELEMENTS(annulusEff_i), ' bad pixels excluded'
     FOR j = 0, n_elements(c_fit) -1 DO BEGIN
        resImage = image0 - c_fit[j] * image_i
        residual[j] = sqrt(total(resImage[annulusEff_i]^2)/n_elements(annulusEff_i))
     ENDFOR
     res_int = interpol(residual, c_fit, c_int,/spline)
     cList[i]= mean(c_int[where(res_int EQ min(res_int))])
     resList[i] = min(res_int)
     sky, (image0 - cList[i] * image_i)[annulusEff_i0], mode, std, /silent
     skylevelList[i] = mode
     skysigList[i] = std
  ENDFOR
  minResId = where(resList EQ min(resList))
  psf_id = satisfyID[minResId]
  c0 = cList[minResId]
  skylevel = skylevelList[minResId]
  skysig = skysigList[minResId]
  xshift = dx[psf_id]
  yshift = dy[psf_id]
  return, [psf_id, c0, skylevel, skysig, secCen[0], secCen[1], xshift, yshift] ; return psf id and c0
END


PRO psf_subtraction, input_fn, output_fn
  COMMON preparedData, cube, infoStruct, nImages, xMesh, yMesh
  restore, input_fn ;; restore data from data preparation PROCEDURE
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
     fitResult = searchPSF(i, satisfyID)
     PSF_id[i] = fitResult[0]
     PSF_amplitude[i] = fitResult[1]
     skyLevel[i] = fitResult[2]
     skySigma[i] = fitResult[3]
     xCenter[i] = fitResult[4]
     yCenter[i] = fitResult[5]
     cube1[*, *, i] = cube[*, *, i] - fitResult[1] * fshift(cube[*, *, fitResult[0]], -fitResult[6], -fitResult[7])
     print, i, ' psf subtracted'
  ENDFOR
  infoStruct1 = add_tag(infoStruct, 'xCenter', xCenter)
  infoStruct1 = add_tag(infoStruct1, 'yCenter', yCenter)
  infoStruct1 = add_tag(infoStruct1, 'PSF_id', PSF_id)
  infoStruct1 = add_tag(infoStruct1, 'PSF_amplitute', PSF_amplitude)
  infoStruct1 = add_tag(infoStruct1, 'sky_level', skyLevel)
  infoStruct1 = add_tag(infoStruct1, 'sky_sigma', skySigma)
  save, cube1, infoStruct1, filename = output_fn
END

PRO aperturePhot, inFn, aperRadius = aperRadius
  IF N_ELEMENTS(aperRadius) EQ 0 THEN aperRadius = 5.0
  restore, inFn
  szCube = size(cube1)
  nImages = szCube[3]
  flux = fltarr(nImages)
  fluxErr = fltarr(nImages)
  f125id = where(infoStruct1.filter EQ 'F125W')
  f160id = where(infoStruct1.filter EQ 'F160W')
  aperList = [aperRadius]
  FOR i = 0, nImages - 1 DO BEGIN
     image = cube1[*, *, i]
     expoTime = infoStruct1.exposure_time[i]
     ;; IF infoList1[f125id[i]].rollAngle EQ 101 THEN $
     ;;    gcntrd, image, 109., 166., xSec, ySec, 2.0 $ ;; search
                ;;    secondary center
     xsec = infoStruct1.xCenter[i]
     ysec = infoStruct1.yCenter[i]
     aper, image * expoTime, xSec, ySec, f, ef, sky, skyerr, $
           1, aperList, [30, 50], [-100, 1e7], /flux, $
           setskyval = [infoStruct1.sky_level[i], infoStruct1.sky_sigma[i] * expoTime, 7000],/silent
     ;; print, 'sky error from aper:', skyerr/expoTime
     ;; print, 'original skyerr:', infoList1[f125id[i]].skysigma
     ;; print, 'optimized aperture radius:', aperList[where(eflux/flux EQ min(eflux/flux))]
     ;; optId = where(eflux/flux EQ min(eflux/flux))
     ;; aperStrList[f125id[i]].aper = aperList
     ;; aperStrList[f125id[i]].flux = flux/expoTime
     ;; aperStrList[f125id[i]].fluxerr = eflux/expoTime
     ;; aperStrList[f125id[i]].aper0 = aperList[optId]
     ;; aperStrList[f125id[i]].filter = 'F125W'
     flux[i] = f[0]/expoTime
     fluxErr[i] = ef[0]/expoTime
  ENDFOR
  infoStruct1 = add_tag(infoStruct1, 'flux', flux)
  infoStruct1 = add_tag(infoStruct1, 'fluxerr', fluxerr)
  forprint, flux, fluxerr, textout = 'aperphot_Dec21.dat'
  save, infoStruct1, file = 'flux_Dec21.sav'
END 