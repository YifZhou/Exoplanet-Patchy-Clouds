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
PRO crosscorr_cen, saveFn
  dataDir = '../data/ABPIC-B/CR_removed/'
  fileList = FILE_SEARCH(STRJOIN([dataDir, '*.fits'], '/'))
  nFile = N_ELEMENTS(fileList)
;  readcol,'crosscorr_result.dat', format = 'x,f,f', xcen0, ycen0
  im01 = mrdfits(fileList[0], 1)
  im02 = mrdfits(fileList[1], 1)
  xy_cen01 = [114.212, 169.284] ;; take the center of first image as a reference
  xy_cen02 = [114.213, 169.284] ;; different filter align with different images
  xcen = fltarr(nFile)
  ycen = fltarr(nFile)
  imSize = size(im01)
  ww = imSize[1]
  FOR i=0, nFile - 1 DO BEGIN
     im_i = mrdfits(fileList[i], 1)
     fn_splited = strsplit(fileList[i], '/', /extract)
     fn = fn_splited[N_ELEMENTS(fn_splited) - 1]
     filter_name = strmid(fn, 19, 5)
     IF filter_name EQ 'F125W' THEN BEGIN 
        cen = ccCenter(im01, im_i, xy_cen01)
        xcen[i] = cen[0]
        ycen[i] = cen[1]
     ENDIF ELSE BEGIN
        cen = ccCenter(im02, im_i, xy_cen02)
        xcen[i] = cen[0]
        ycen[i] = cen[1]
     ENDELSE 
     fileList[i] = fn
  ENDFOR
  forprint, fileList, xcen, ycen, textout = saveFn,/nocomment , width = 120 ;;
END

FUNCTION ccCenter, im0, im1, cen0
  corr = crosscorr(im0, im1, pmax, dxy, range = 10)
  cen10 = cen0 + dxy
  xy_low0 = floor(cen0 - 20)
  subim0 = im0[xy_low0[0]:xy_low0[0] + 41, xy_low0[1]:xy_low0[1] + 41]
  xy_low1 = floor(cen10 - 20)
  subim1 = im1[xy_low1[0]:xy_low1[0] + 41, xy_low1[1]:xy_low1[1] + 41]
  corr = crosscorr(subim0, subim1, pmax, dxy1)
  dxy2 = xy_low1 - xy_low0 + dxy1
  print, dxy, dxy2
  return, cen0 + dxy2
END


PRO WCS_cen, saveFn
  dataDir = '../data/ABPIC-B/CR_removed/'
  fileList = FILE_SEARCH(STRJOIN([dataDir, '*.fits'], '/'))
  nFile = N_ELEMENTS(fileList)
  im01 = mrdfits(fileList[0], 1, hd01)
  xy_cen01 = [114.212, 169.284] ;; take the center of first image as a reference
  xcen = fltarr(nFile)
  ycen = fltarr(nFile)
  imSize = size(im01)
  ww = imSize[1]
  FOR i=0, nFile - 1 DO BEGIN
     im_i = mrdfits(fileList[i], 1, hd_i)
     fn_splited = strsplit(fileList[i], '/', /extract)
     fn = fn_splited[N_ELEMENTS(fn_splited) - 1]
     xyxy, hd01, hd_i, xy_cen01[0], xy_cen01[1], x0, y0
     xcen[i] = x0
     ycen[i] = y0
     fileList[i] = fn
  ENDFOR
  forprint, fileList, xcen, ycen, textout = saveFn,/nocomment , width = 120 ;;
END 
