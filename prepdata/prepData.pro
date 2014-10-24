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
PRO prepData, target, saveFN
  infoStruct = {info, filter:'', exposureTime:0, data_obs:'', time_obs:''}
  dataDir = STRJOIN(['/home/yzhou/Documents/Exoplanet_Patchy_Project/data', target, 'CR_removed'], '/')
  fitsFNList = FILE_SEARCH(STRJOIN([dataDir, '*.fits'], '/'))
  nFile = N_ELEMENTS(fitsFNList)
  xcen = fltarr(nFile)
  ycen = fltarr(nFile)
  cube = MAKE_ARRAY(256, 256, nFile, /DOUBLE)
  FOR i = 0, nFile -1 DO BEGIN
     im0 = mrdfits(fitsFNList[i], 0, header0) ;; read primary header
     im = mrdfits(fitsFNList[i], 1, header1)
     ;;cntrd, im, 120., 170., x0, y0, 3.7, extendbox = 20 ;; use cntrd
     ;;to find the centroid of the primary object
     cntrd, im, 120., 170., x00, y00, 3.7, extendbox = 20 ;; use cntrd to find the approximate center
     gcntrd, im, x00, y00, x0, y0, 3.7, maxgood = 1e6 ;; use gcntrd to find the center again
     xcen[i] = x00
     ycen[i] = y00
;;   print, fitsFNList[i], x0, y0
  ENDFOR
  forprint,xcen, ycen, textout = 'cntrd_result.dat',/nocomment ;;
  ;;print out center to test

end


  
