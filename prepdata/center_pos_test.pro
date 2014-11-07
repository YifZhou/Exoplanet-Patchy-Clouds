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
PRO center_pos_test, method
  target = 'ABPIC-B'
  dataDir = STRJOIN(['/home/yzhou/Documents/Exoplanet_Patchy_Project/data', target, 'CR_removed'], '/')
  fitsFNList = FILE_SEARCH(STRJOIN([dataDir, '*.fits'], '/'))
  nFile = N_ELEMENTS(fitsFNList)
  CASE method OF
     'cntrd': readcol, 'cntrd_result.dat', format = 'x, f, f', xcen, ycen
     'gcntrd': readcol, 'gcntrd_result.dat', format = 'x, f, f', xcen, ycen
     'crosscorr': BEGIN
        readcol, 'crosscorr_result.dat', format = 'x, f, f', xcen, ycen
        im01 = mrdfits(fitsFNList[0], 1, hd)
        im02 = mrdfits(fitsFNList[13], 1, hd)
        xy_cen01 = [114.356, 169.259] ;; take the center of first image as a reference
        xy_cen02 = [130.276, 177.494]
        ww = 256.
     END
  ENDCASE
  xoff = fltarr(nFile)
  yoff = fltarr(nFile)
  FOR i = 0, nFile - 1 DO BEGIN
     im = mrdfits(fitsFNList[i], 1, hd)
     imShifted = fshift(im, !pi, exp(1)) ;; shift pi in x direction, shift e in y direction
     CASE method OF
        'cntrd': BEGIN
           cntrd, imShifted, xcen[i] + !pi, ycen[i] + exp(1), x_i, y_i, 1.59
           xoff[i] = x_i - xcen[i] - !pi
           yoff[i] = y_i - ycen[i] - exp(1)
        END
        'gcntrd': BEGIN
           gcntrd, imShifted, xcen[i] + !pi, ycen[i] + exp(1), x_i, y_i, 1.59
           xoff[i] = x_i - xcen[i] - !pi
           yoff[i] = y_i - ycen[i] - exp(1)
        END
        'crosscorr': BEGIN
           fn_splited = strsplit(fitsFNList[i], '/', /extract)
           fn = fn_splited[N_ELEMENTS(fn_splited) - 1]
           orbit = fix(strmid(fn, 6, 2)) ;; get the orbit number
           IF orbit MOD 2 EQ 1 THEN BEGIN 
              corr = crosscorr(im01, imShifted, pmax)
              IF pmax(0) GE 0. THEN dx =  ww/2. - pmax(0) ELSE dx =  -ww/2. + abs(pmax(0))
              IF pmax(1) GE 0. THEN dy =  ww/2. - pmax(1) ELSE dy =  -ww/2. + abs(pmax(1))
              xoff[i] = xy_cen01[0] + dx - xcen[i] - !pi
              yoff[i] = xy_cen01[1] + dy - ycen[i] - exp(1)
           ENDIF ELSE BEGIN
              corr = crosscorr(im02, imShifted, pmax)
              IF pmax(0) GE 0. THEN dx =  ww/2. - pmax(0) ELSE dx =  -ww/2. + abs(pmax(0))
              IF pmax(1) GE 0. THEN dy =  ww/2. - pmax(1) ELSE dy =  -ww/2. + abs(pmax(1))
              xoff[i] = xy_cen02[0] + dx - xcen[i] - !pi
              yoff[i] = xy_cen02[1] + dy - ycen[i] - exp(1)
           ENDELSE
        END 
     ENDCASE     
  ENDFOR
  forprint, xoff, yoff, textout = method + '_off.dat', /nocomment
END

PRO center_pos_test2, method
  loop = 1000
  xoff = fltarr(loop)
  yoff = fltarr(loop)
  dxList = fltarr(loop)
  dyList = fltarr(loop)
  
  image = mrdfits('~/Documents/Exoplanet_Patchy_Project/data/ABPIC-B/CR_removed/orbit_07_dither_02_F160W.fits', 1, hd)
  ww = 256
  OverSample = 10.
  imageOverSamp = congrid(image, OverSample * ww, OverSample * ww, cubic = -0.5)
  x0 = 114.212
  y0 = 169.284
  FOR i = 0, loop - 1 DO BEGIN
     step = 10 * randomu(seed)
     dx = step * randomn(seed)
     dy = step * randomn(seed)
     ;; imShiftedOverSamp = fshift(imageOverSamp, dx * OverSample, dy * OverSample)
     ;; imShifted = congrid(imShiftedOverSamp, ww, ww, cubic = -0.5)
     imshifted = fshift(image, dx, dy)
     image0 = image
     ;; nNoise = ceil(5 * randomu(seed))
     ;; FOR j = 1, nNoise DO BEGIN
     ;;    imshifted = imshifted + 500 * psf_gaussian(npixel = 256, centroid = [255 *randomu(seed), 255*randomu(seed)], fwhm = 1.8)
     ;;    image0 = image0 + 500 * psf_gaussian(npixel = 256, centroid = [255 *randomu(seed), 255*randomu(seed)], fwhm = 1.8)
     ;; ENDFOR
     CASE method OF
        'cntrd': BEGIN
           cntrd, image, x0, y0, xcen, ycen, 1.79
           cntrd, imShifted, xcen + dx, ycen + dy, x_i, y_i, 1.79
           xoff[i] = x_i - xcen - dx
           yoff[i] = y_i - ycen - dy
           print, dx, dy, x_i - (xcen + dx), y_i - (ycen + dy)
        END
        'gcntrd': BEGIN
           gcntrd, imShifted, xcen + dx, ycen + dy, x_i, y_i, 3.0
           xoff[i] = x_i - xcen - dx
           yoff[i] = y_i - ycen - dy
        END
        'crosscorr': BEGIN
           corr = crosscorr(image0, imShifted, pmax, dxy, range = 10)
           ;IF pmax(0) GE 0. THEN dx0 =  ww/2. - pmax(0) ELSE dx0 =  -ww/2. + abs(pmax(0))
                                ;IF pmax(1) GE 0. THEN dy0 =  ww/2. -
                                ;pmax(1) ELSE dy0 =  -ww/2. +
                                ;abs(pmax(1))
           dx0 = dxy[0]
           dy0 = dxy[1]
           xoff[i] = dx0 - dx
           yoff[i] = dy0 - dy
           dxList[i] = dx
           dyList[i] = dy
           print, strn(i), 'finished'
        END 
     ENDCASE     
  ENDFOR
  forprint, dxList, dyList, xoff, yoff, textout = method + '_cenTest2.dat',/nocomment
END


  

  