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
FUNCTION my_shift2d, im, shiftxy, cubic = cubic
  sz = size(im)
  xlen = sz[1]
  ylen = sz[2]
  x0 = findgen(xlen)
  y0 = findgen(ylen)
  xnew = x0 - shiftxy[0]
  xnew = xnew - xlen * floor(xnew / xlen)
  ynew = y0 - shiftxy[1]
  ynew = ynew - ylen * floor(ynew / ylen)
  IF N_ELEMENTS(cubic) EQ 0 THEN cubic = -0.5
  IF cubic NE 0 THEN imnew = interpolate(im, xnew, ynew, /grid, cubic=cubic) ELSE imnew = interpolate(im, xnew, ynew, /grid)
  return, imnew  
END
  