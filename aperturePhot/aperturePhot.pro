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
PRO aperturePhot, inFn, aperRadius = aperRadius
  aperStr = {aper:fltarr(31), flux:fltarr(31), fluxerr:fltarr(31), aper0:0., filter:''}
  IF N_ELEMENTS(aperRadius) EQ 0 THEN aperRadius = 5.0
  restore, inFn
  aperStrList = REPLICATE(aperStr, N_ELEMENTS(infoList1))
  meshgrid, findgen(256), findgen(256), xMesh, yMesh
  f125id = where(infoList1.filter EQ infoList1[0].filter)
  f160id = where(infoList1.filter EQ infoList1[1].filter)
  f125Flux = fltarr(N_ELEMENTS(f125id))
  f160Flux = fltarr(N_ELEMENTS(f160id))
  aperList = 2 + findgen(31) * 0.1
  FOR i = 0, N_ELEMENTS(f125id) - 1 DO BEGIN
     print, f125id[i]
     image = cube1[*, *, f125id[i]]
     expoTime = infoList1[f125id[i]].exposureTime
     IF infoList1[f125id[i]].rollAngle EQ 101 THEN $
        gcntrd, image, 109., 166., xSec, ySec, 2.0 $ ;; search secondary center
     ELSE gcntrd, image, 126., 172., xsec, ysec, 2.0
     disSec = sqrt((xMesh - xSec)^2 + (yMesh - ySec)^2) ;; distance to secondary array
                                ;f125Flux[i] =
                                ;total(image[where(disSec LE
                                ;aperRadius)] -
                                ;infoList1[f125id[i]].skylevel)
     aper, image * expoTime, xSec, ySec, flux, eflux, sky, skyerr, $
           1, aperList, [30, 50], [-100, 1e7], /flux, $
           setskyval = [infoList1[f125id[i]].skylevel, infoList1[f125id[i]].skysigma * expoTime, 7000],/silent
     print, 'sky error from aper:', skyerr/expoTime
     print, 'original skyerr:', infoList1[f125id[i]].skysigma
     print, 'optimized aperture radius:', aperList[where(eflux/flux EQ min(eflux/flux))]
     optId = where(eflux/flux EQ min(eflux/flux))
     aperStrList[f125id[i]].aper = aperList
     aperStrList[f125id[i]].flux = flux/expoTime
     aperStrList[f125id[i]].fluxerr = eflux/expoTime
     aperStrList[f125id[i]].aper0 = aperList[optId]
     aperStrList[f125id[i]].filter = 'F125W'
  ENDFOR

  FOR i = 0, N_ELEMENTS(f160id) - 1 DO BEGIN
     print, f160id[i]
     image = cube1[*, *, f160id[i]]
     expoTime = infoList1[f160id[i]].exposureTime
     IF infoList1[f160id[i]].rollAngle EQ 101 THEN $
        gcntrd, image, 109., 166., xSec, ySec, 2.0 $ ;; search secondary center
     ELSE gcntrd, image, 126., 172., xsec, ysec, 2.0
     ;disSec = sqrt((xMesh - xSec)^2 + (yMesh - ySec)^2) ;; distance to secondary array
     ;f160Flux[i] = total(image[where(disSec LE aperRadius)] - infoList1[f160id[i]].skylevel)
     aper, image * expoTime, xSec, ySec, flux, eflux, sky, skyerr, $
           1, aperList, [30, 50], [-100, 1e7], /flux, $
           setskyval = [infoList1[f160id[i]].skylevel, infoList1[f160id[i]].skysigma * expoTime, 7000],/silent
     print, 'sky error from aper:', skyerr/expoTime
     print, 'original skyerr:', infoList1[f160id[i]].skysigma
     print, 'optimized aperture radius:', aperList[where(eflux/flux EQ min(eflux/flux))]
     optId = where(eflux/flux EQ min(eflux/flux))
     aperStrList[f160id[i]].aper = aperList
     aperStrList[f160id[i]].flux = flux/expoTime
     aperStrList[f160id[i]].fluxerr = eflux/expoTime
     aperStrList[f160id[i]].aper0 = aperList[optId]
     aperStrList[f160id[i]].filter = 'F160W'
  ENDFOR
  ;; save, f160Flux, f160Flux, file = 'aperphot.sav'
  ;; forprint, infoList1[f160id].obsDate, infoList1[f160id].obsTime, f160Flux, textout = 'f160aperphot.dat'
  ;; forprint, infoList1[f160id].obsDate, infoList1[f160id].obsTime,
  ;; f160Flux, textout = 'f160aperphot.dat'
  save, aperStrList, file = 'aperPhot_Nov_14.sav'
END 