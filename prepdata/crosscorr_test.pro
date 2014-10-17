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
PRO crosscorr_test
  dataDir = '../data/ABPIC-B/CR_removed/'
  fileList = FILE_SEARCH(STRJOIN([dataDir, '*.fits'], '/'))
  nFile = N_ELEMENTS(fileList)
  im01 = mrdfits(fileList[0], 1, hd)
  im02 = mrdfits(fileList[13], 1, hd)
  xy_cen01 = [114.356, 169.259] ;; take the center of first image as a reference
  xy_cen02 = [130.276, 177.494]
  xcen = fltarr(nFile)
  ycen = fltarr(nFile)
  imSize = size(im01)
  ww = imSize[1]
  FOR i=0, nFile - 1 DO BEGIN
     im_i = mrdfits(fileList[i], 1, hd)
     fn_splited = strsplit(fileList[i], '/', /extract)
     fn = fn_splited[N_ELEMENTS(fn_splited) - 1]
     orbit = fix(strmid(fn, 6, 2)) ;; get the orbit number
     IF orbit MOD 2 EQ 1 THEN BEGIN 
        corr = crosscorr(im01, im_i, pmax)
        IF pmax(0) GE 0. THEN dx =  ww/2. - pmax(0) ELSE dx =  -ww/2. + abs(pmax(0))
        IF pmax(1) GE 0. THEN dy =  ww/2. - pmax(1) ELSE dy =  -ww/2. + abs(pmax(1))
        xcen[i] = xy_cen01[0] + dx
        ycen[i] = xy_cen01[1] + dy
     ENDIF ELSE BEGIN
        corr = crosscorr(im02, im_i, pmax)
        IF pmax(0) GE 0. THEN dx =  ww/2. - pmax(0) ELSE dx =  -ww/2. + abs(pmax(0))
        IF pmax(1) GE 0. THEN dy =  ww/2. - pmax(1) ELSE dy =  -ww/2. + abs(pmax(1))
        xcen[i] = xy_cen02[0] + dx
        ycen[i] = xy_cen02[1] + dy
     ENDELSE
     fileList[i] = fn
  ENDFOR
  forprint, fileList, xcen, ycen, textout = 'crosscorr_result.dat',/nocomment , width = 120;;
END 

PRO WCS_test
  dataDir = '../data/ABPIC-B/CR_removed/'
  fileList = FILE_SEARCH(STRJOIN([dataDir, '*.fits'], '/'))
  nFile = N_ELEMENTS(fileList)
  im01 = mrdfits(fileList[0], 1, hd01)
  im02 = mrdfits(fileList[13], 1, hd02)
  xy_cen01 = [114.356, 169.259] ;; take the center of first image as a reference
  xy_cen02 = [130.276, 177.494]
  xcen = fltarr(nFile)
  ycen = fltarr(nFile)
  imSize = size(im01)
  ww = imSize[1]
  FOR i=0, nFile - 1 DO BEGIN
     im_i = mrdfits(fileList[i], 1, hd_i)
     fn_splited = strsplit(fileList[i], '/', /extract)
     fn = fn_splited[N_ELEMENTS(fn_splited) - 1]
     orbit = fix(strmid(fn, 6, 2)) ;; get the orbit number
     IF orbit MOD 2 EQ 1 THEN BEGIN 
        xyxy, hd01, hd_i, xy_cen01[0], xy_cen01[1], x0, y0
        xcen[i] = x0
        ycen[i] = y0
     ENDIF ELSE BEGIN
        xyxy, hd02, hd_i, xy_cen02[0], xy_cen02[1], x0, y0
        xcen[i] = x0
        ycen[i] = y0
     ENDELSE
     fileList[i] = fn
  ENDFOR
  forprint, fileList, xcen, ycen, textout = 'WCS_result.dat',/nocomment , width = 120;;
END 
