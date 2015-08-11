;; simple photon noise

PRO calError, F125Error, F160Error
  dataDIR = '../data/2M1207B/'
  F125InfoFN = '2015_Jun_24TinyTimF125Result.csv'
  F125Info = myReadCSV(F125InfoFN, ['filename', 'filter', 'orbit', 'PosAngle', 'dither', 'exposureset', 'obsdate', 'obstime', 'expoTime', 'FLUXA', 'FLUXB', 'SKY', 'PRIMARY_X', 'PRIMARY_Y', 'SECONDARY_X', 'SECONDARY_Y', 'CHISQ'])
  F125Error = fltarr(n_elements(F125Info.filename))
  FOR i=0, n_elements(F125Info.filename) - 1 DO BEGIN
     err = mrdfits(dataDIR + F125Info.filename[i], 2,/silent) ;; read the error array
     meshgrid, findgen(256), findgen(256), xx, yy
     dist = sqrt((xx - F125Info.secondary_x[i])^2 + (yy - F125Info.secondary_y[i])^2)
     inAperID = where(dist LE 3.0) ;; use an aperture of 3 to determine the photon noise level
     F125Error[i] = sqrt(total(err[inAperID]^2))
  ENDFOR

  F160InfoFN = '2015_Jun_24TinyTimF160Result.csv'
  F160Info = myReadCSV(F160InfoFN, ['filename', 'filter', 'orbit', 'PosAngle', 'dither', 'exposureset', 'obsdate', 'obstime', 'expoTime', 'FLUXA', 'FLUXB', 'SKY', 'PRIMARY_X', 'PRIMARY_Y', 'SECONDARY_X', 'SECONDARY_Y', 'CHISQ'])
  F160Error = fltarr(n_elements(F160Info.filename))
  FOR i=0, n_elements(F160Info.filename) - 1 DO BEGIN
     err = mrdfits(dataDIR + F160Info.filename[i], 2,/silent) ;; read the error array
     meshgrid, findgen(256), findgen(256), xx, yy
     dist = sqrt((xx - F160Info.secondary_x[i])^2 + (yy - F160Info.secondary_y[i])^2)
     inAperID = where(dist LE 3.0) ;; use an aperture of 3 to determine the photon noise level
     F160Error[i] = sqrt(total(err[inAperID]^2))
  ENDFOR
  F125Error = F125Error/F125Info.FLUXB
  F160Error = F160Error/F160Info.FLUXB
  print, mean(F125Error)
  print, mean(F160Error)
END
