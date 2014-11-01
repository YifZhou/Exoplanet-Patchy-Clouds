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
  IF N_ELEMENTS(aperRadius) EQ 0 THEN aperRadius = 5.0
  restore, inFn
  meshgrid, findgen(256), findgen(256), xMesh, yMesh
  f125id = where(infoList1.filter EQ infoList1[0].filter)
  f160id = where(infoList1.filter EQ infoList1[1].filter)
  f125Flux = fltarr(N_ELEMENTS(f125id))
  f160Flux = fltarr(N_ELEMENTS(f160id))
  FOR i = 0, N_ELEMENTS(f125id) - 1 DO BEGIN
     print, f125id[i]
     image = cube1[*, *, f125id[i]]
     IF infoList1[f125id[i]].rollAngle EQ 101 THEN $
        gcntrd, image, 109., 166., xSec, ySec, 2.0 $ ;; search secondary center
     ELSE gcntrd, image, 126., 172., xsec, ysec, 2.0
     disSec = sqrt((xMesh - xSec)^2 + (yMesh - ySec)^2) ;; distance to secondary array
     f125Flux[i] = total(image[where(disSec LE aperRadius)] - infoList1[f125id[i]].skylevel)
  ENDFOR

  FOR i = 0, N_ELEMENTS(f160id) - 1 DO BEGIN
     print, f160id[i]
     image = cube1[*, *, f160id[i]]
     IF infoList1[f160id[i]].rollAngle EQ 101 THEN $
        gcntrd, image, 109., 166., xSec, ySec, 2.0 $ ;; search secondary center
     ELSE gcntrd, image, 126., 172., xsec, ysec, 2.0
     disSec = sqrt((xMesh - xSec)^2 + (yMesh - ySec)^2) ;; distance to secondary array
     f160Flux[i] = total(image[where(disSec LE aperRadius)] - infoList1[f160id[i]].skylevel)
  ENDFOR
  save, f125Flux, f160Flux, file = 'aperphot.sav'
  forprint, infoList1[f125id].obsDate, infoList1[f125id].obsTime, f125Flux, textout = 'f125aperphot.dat'
  forprint, infoList1[f160id].obsDate, infoList1[f160id].obsTime, f160Flux, textout = 'f160aperphot.dat'
END 