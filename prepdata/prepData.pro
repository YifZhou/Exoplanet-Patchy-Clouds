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
PRO prepData, target, shiftMethod, saveFN
  infoStruct = {filter:'', exposureTime:0., obsDate:'', obsTime:'', rollAngle:0.0, orbit:0, dither:0, xShift:0., yShift:0.}
  dataDir = STRJOIN(['/home/yzhou/Documents/Exoplanet_Patchy_Project/data', target, 'CR_removed'], '/')
  fitsFNList = FILE_SEARCH(STRJOIN([dataDir, '*.fits'], '/'))
  nFile = N_ELEMENTS(fitsFNList)
  xcen = fltarr(nFile)
  ycen = fltarr(nFile)
  cube = MAKE_ARRAY(256, 256, nFile, /DOUBLE) ;; list to save images
  infoList = replicate(infoStruct, nFile);; list to save header information
  readcol, 'centroid_cc.dat', format = 'x,f,f', xcen, ycen, /SILENT
  imageSz = 256
  overSampFactor = 50
  FOR i = 0, nFile -1 DO BEGIN
     fn_splited = strsplit(fitsFNList[i], '/', /extract)
     fileName0 = fn_splited[N_ELEMENTS(fn_splited) - 1]
     orbit = fix(strmid(fileName0, 6, 2))
     dither = fix(strmid(fileName0, 16, 2))
     IF orbit MOD 2 EQ 0 THEN infoList[i].rollAngle = 129. ELSE infoList[i].rollAngle = 101. ;; ortib number determines rolling angle
     
     im0 = mrdfits(fitsFNList[i], 0, header0) ;; read primary header
     im = mrdfits(fitsFNList[i], 1, header1)
     ;; shift the image so that the primary star's image
     ;; centered at (127, 127)
     dx = 127. - xcen[i]
     dy = 127. - ycen[i]
     IF strlowcase(shiftMethod) EQ 'fshift' THEN BEGIN
        ;imOverSamp = congrid(im, imageSz * overSampFactor, imageSz * overSampFactor, cubic = -0.5)
        im_i = fshift(im, dx , dy)
        ;im_i = congrid(imiOS, imageSz, imageSz, cubic = -0.5)
     ENDIF ELSE IF strlowcase(shiftMethod) EQ 'bicubic' THEN im_i = my_shift2d(im, [dx, dy]) $
           ELSE im_i = im
     infoList[i].filter = fxpar(header0, 'filter')
     infoList[i].exposureTime = fxpar(header0, 'exptime')
     infoList[i].obsDate = fxpar(header0, 'date-obs')
     infoList[i].obsTime = fxpar(header0, 'time-obs')
     infoList[i].orbit = orbit
     infoList[i].dither = dither
     infoList[i].xShift = dx
     infoList[i].yShift = dy
     cube[*,*, i] = im_i
     print,'i',' image finished'
  ENDFOR
  save, cube, infoList, filename = saveFN
  ;;print out center to test

end


  
