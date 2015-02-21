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
PRO aperturePhotPipeLine2, infoFile, fileType, aperRadius  = aperRadius, subtract = Subtract
  fileInfo = myReadCSV(infoFile, ['filename', 'filter', 'orbit', 'posang', 'dither', 'exposure_set','obs_date','obs_time','exposure_time'])
  IF N_elements(Subtract) EQ 0 THEN subtract = 1
  dataDir = '../data/ABPIC-B_myfits/' ;; changable
  ;; read the first images for two filters, as the reference images
     im125 = mrdfits('../data/ABPIC-B/icdg07p3q_flt.fits', 1, hd)
     im160 = mrdfits('../data/ABPIC-B/icdg07p7q_flt.fits', 1, hd) ;; define cross correlation reference image
  IF fileType EQ 'flt' THEN BEGIN
     preparedFN = prepData(fileInfo, dataDir, im125, im160)
     PSF_fn = 'flt_PSF.sav'
  ENDIF ELSE IF fileType EQ 'ima' THEN BEGIN
     preparedFN = prepImaData(fileInfo, dataDIR, im125, im160)
     PSF_fn = 'ima_PSF.sav'
  ENDIF ELSE IF fileType EQ 'myfits' THEN BEGIN
     preparedFN = prepData(fileInfo, dataDIR, im125, im160)
     PSF_fn = 'myfits_PSF.sav'
  ENDIF 
  subtractedFN = psf_subtraction(preparedFN, PSF_fn, Subtract)
  IF n_elements(aperRadius) EQ 0 THEN aperRadius = 5
  resultFN = aperturePhot(subtractedFN, aperRadius = 5)
  resultCSVFN = filename() + '_' + fileType + '_aper=' + strn(aperRadius) + '_result.csv'
  spawn, 'python sav2csv.py ' + resultFN + ' ' + resultCSVFN ;; convert .sav file to csv file for easier using.
END

FUNCTION myReadCSV,fn, tags
  ;; function for reading csv files
  ;; change the names of tags
  strct = read_csv(fn)
  return, rename_tags(strct, ['FIELD01','FIELD02','FIELD03','FIELD04','FIELD05','FIELD06','FIELD07','FIELD08','FIELD09'], tags)
END

FUNCTION prepData, infoStruct, dataDir, im125, im160
  ;; apply no shift to the image
      ;; process F125 and F160 individually
  F125ID = where(infoStruct.filter EQ 'F125W')
  F160ID = where(infoStruct.filter EQ 'F160W')

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
     print,'i',' image finished preparation'
  ENDFOR
  infoStruct = add_tag(infoStruct, 'xoff', xoff)
  infoStruct = add_tag(infoStruct, 'yoff', yoff)
  saveFN = filename() + '_prepared.sav'
  save, cube, infoStruct, filename = saveFN
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

FUNCTION searchPSF, id0, satisfyID
  ;; deal with the unaligned prepared images
  COMMON preparedData, cube, PSFLIST, infoList, nImages, xMesh, yMesh
  imSize = (size(cube))[1] ;; ima file is 266*266
  primaryCen = [114.212, 169.284] + (imSize - 256)/2. ;; center of the primary star on the reference image (the very first image)
  dx = PSFLIST[satisfyID].xoff - infoList.xoff[id0]
  dy = PSFLIST[satisfyID].yoff - infoList.yoff[id0]
  d2Int = (dx - round(dx))^2 + (dy - round(dy))^2 ;; fractional part of the shift
  ID_i = (where(d2Int EQ min(d2Int)))[0]
  PSF_id = satisfyID[ID_i] ;; choose the satisfied PSF that has the smallest fractional pixel shift so that PSF change is the smallest


  disPrimary = sqrt((xMesh - (primaryCen[0] + infoList.xoff[id0]))^2 + (yMesh - (primaryCen[1] + infoList.yoff[id0]))^2)
  secCen1 = [95., 209.] + (imSize - 256)/2. ;; approximate center of the secondary star
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
     
  disSecondary = sqrt((xMesh - secCen[0])^2 + (yMesh - secCen[1])^2)
  annulusPri = where((disPrimary GE 30) AND (disPrimary LE 60))
  annulusSec = where(disSecondary LE 15)
  annulusEff = cgsetdifference(annulusPri, annulusSec)
  c_fit = 0.99 + 0.002*findgen(11)
  c_int = congrid(c_fit, 200,/interp)
  residual = fltarr(N_ELEMENTS(c_fit))
  image_i = fshift(PSFList[PSF_id].PSF, -dx[ID_i], -dy[ID_i])
  IF infoList.posang[PSF_id] le 110 THEN BEGIN
     x0 = secCen1[0] + (infoList.dither[PSF_id] MOD 2) * 10.2 -dx[ID_i]
     y0 = secCen1[1] + (infoList.dither[PSF_id]/2) * 10.2 - dy[ID_i]
     secCen_i = findPeak(image_i, x0, y0, range = 5) 
  ENDIF ELSE BEGIN
     x0 = secCen2[0] + (infoList.dither[PSF_id] MOD 2) * 10.2 - dx[ID_i]
     y0 = secCen2[1] + (infoList.dither[PSF_id]/2) * 10.2 - dy[ID_i]
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
  amp = mean(c_int[where(res_int EQ min(res_int))])
  residual = min(res_int)
  sky, (image0 - amp * image_i)[annulusEff_i0], mode, std, /silent
  skylevel = mode
  skysig = std
  xshift = dx[ID_i]
  yshift = dy[ID_i]
  return, [psf_id, amp, skylevel, skysig, secCen[0], secCen[1], xshift, yshift] ; return psf id and c0
END


FUNCTION psf_subtraction, input_fn, PSF_fn, Subtract
  COMMON preparedData, cube, PSFLIST, infoStruct, nImages, xMesh, yMesh
  restore, input_fn ;; restore data from data preparation PROCEDURE
  restore, PSF_fn
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
     satisfyID = where((PSFList.filter EQ filter_i) AND (PSFList.rollAngle NE angle_i))
     fitResult = searchPSF(i, satisfyID)
     PSF_id[i] = fitResult[0]
     PSF_amplitude[i] = fitResult[1]
     skyLevel[i] = fitResult[2]
     skySigma[i] = fitResult[3]
     xCenter[i] = fitResult[4]
     yCenter[i] = fitResult[5]
     IF Subtract NE 0 THEN cube1[*, *, i] = cube[*, *, i] - fitResult[1] * fshift(PSFLIST[fitResult[0]].PSF, -fitResult[6], -fitResult[7]) $
                                       ELSE cube1[*,*,i] = cube[*,*,i]
     print, i, ' image finished psf subtraction'
  ENDFOR
  infoStruct1 = add_tag(infoStruct, 'xCenter', xCenter)
  infoStruct1 = add_tag(infoStruct1, 'yCenter', yCenter)
  infoStruct1 = add_tag(infoStruct1, 'PSF_id', PSF_id)
  infoStruct1 = add_tag(infoStruct1, 'PSF_amplitute', PSF_amplitude)
  infoStruct1 = add_tag(infoStruct1, 'sky_level', skyLevel)
  infoStruct1 = add_tag(infoStruct1, 'sky_sigma', skySigma)
  output_fn = filename() + '_subtracted.sav'
  save, cube1, infoStruct1, filename = output_fn
  return, output_fn
END

FUNCTION aperturePhot, inFn, aperRadius = aperRadius
  IF N_ELEMENTS(aperRadius) EQ 0 THEN aperRadius = 5.0
  restore, inFn
  szCube = size(cube1)
  nImages = szCube[3]
  flux = fltarr(nImages)
  fluxErr = fltarr(nImages)
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
     fluxErr[i] = ef[0]/expoTime
     print, i, ' image finished photometry'
  ENDFOR
  infoStruct1 = add_tag(infoStruct1, 'flux', flux)
  infoStruct1 = add_tag(infoStruct1, 'fluxerr', fluxerr)
  infoStruct1 = add_tag(infoStruct1, 'xFWHM', xFWHM)
  infoStruct1 = add_tag(infoStruct1, 'yFWHM', yFWHM)
  output_fn =  filename() + '_aperPhot.sav'
  save, infoStruct1, file = output_fn
  return, output_fn
END

FUNCTION filename
  time = systime()
  mm = strmid(time, 4, 3)
  dd = string(uint(strmid(time, 8, 2)), format = '(I2.2)')
  year = strmid(time, 20, 4)
  fn = year + '_' + mm + '_' + dd
  return, fn
END
