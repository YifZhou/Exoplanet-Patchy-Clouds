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
PRO shift_test, im0
  step = 100
  abs_change1 = fltarr(step)
  flux_change1 = fltarr(step)
  abs_change2 = fltarr(step)
  flux_change2 = fltarr(step)
  
  n_pixels = 256. * 256.
  im_i = im0
  step_l = (1 + findgen(100)) * 0.2
  FOR i = 0, step - 1 DO BEGIN
     dx = step_l[i] * randomn(seed, /uniform)
     dy = step_l[i] * randomn(seed, /uniform)
     im_i0 = my_shift2d(im0, [dx, dy])
     im_i = my_shift2d(im_i0, [-dx, -dy])
     abs_change1[i] = sqrt(total((im_i - im0)^2)) / n_pixels
     flux_change1[i] = total(im_i - im0) / n_pixels

     im_i0 = fshift(im0, dx, dy)
     im_i = fshift(im_i0, -dx, -dy)
     abs_change2[i] = sqrt(total((im_i - im0)^2)) / n_pixels
     flux_change2[i] = total(im_i - im0) / n_pixels
  ENDFOR
  forprint, step_l, abs_change1, flux_change1, textout = 'cubic3_shiftchange.dat',/nocomment
  forprint, step_l, abs_change2, flux_change2, textout = 'fshift_shiftchange.dat',/nocomment
END


     