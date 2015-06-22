PRO combineResidual
  ;;; median combine the residual
  ;;; prepare for a residual included fitting
  ;;; generate residual for each individual position

  ;;;; F125W
  F125InfoFN = '2M1207B_flt_F125W_fileInfo.csv'
  F125INFO = myReadCSV(F125InfoFN, ['filename', 'filter', 'orbit', 'PosAngle', 'dither', 'exposureset', 'obsdate', 'obstime', 'expoTime'])
  residual= fltarr(27, 27, 8)
  F125INFO.posangle[where(F125INFO.posangle EQ 202.0)] = 0
  F125INFO.posangle[where(F125INFO.posangle EQ 227.0)] = 1
  FOREACH angle, [0, 1] DO BEGIN
    FOREACH dither, [0, 1, 2, 3] DO BEGIN
       IDList = where((F125INFO.posangle EQ angle) AND (F125INFO.dither EQ dither))
       residualCube = fltarr(27, 27, n_elements(IDList)) ;; a temporary cube to save the residual for every individual exposure
       FOR i = 0, n_elements(IDList) - 1 DO BEGIN
          id = IDList[i]
          fn = './fitsResult/' + strmid(F125INFO.filename[id], 0, 9) + '.fits' ;;;saved fitting result fits file
          im = mrdfits(fn, 0, /silent)
          psf = mrdfits(fn, 1, /silent)
          residualCube[*, *, i] = im - psf ;;;save the residual for every individual exposure
       ENDFOR
       residual[*, *, angle*4 + dither] = median(residualCube, dimension=3)       
    ENDFOREACH
  ENDFOREACH
  save, residual, file = 'F125W_residual.sav'

  ;;;; F160W
  F160InfoFN = '2M1207B_flt_F160W_fileInfo.csv'
  F160INFO = myReadCSV(F160InfoFN, ['filename', 'filter', 'orbit', 'PosAngle', 'dither', 'exposureset', 'obsdate', 'obstime', 'expoTime'])
  F160INFO.posangle[where(F160INFO.posangle EQ 202.0)] = 0
  F160INFO.posangle[where(F160INFO.posangle EQ 227.0)] = 1
  FOREACH angle, [0, 1] DO BEGIN
     FOREACH dither, [0, 1, 2, 3] DO BEGIN
       IDList = where((F160INFO.posangle EQ angle) AND (F160INFO.dither EQ dither))
       residualCube = fltarr(27, 27, n_elements(IDList)) ;; a temporary cube to save the residual for every individual exposure
       FOR i = 0, n_elements(IDList) - 1 DO BEGIN
          id = IDList[i]
          fn = './fitsResult/' + strmid(F160INFO.filename[id], 0, 9) + '.fits' ;;;saved fitting result fits file
          im = mrdfits(fn, 0, /silent)
          psf = mrdfits(fn, 1, /silent)
          residualCube[*, *, i] = im - psf ;;;save the residual for every individual exposure
       ENDFOR
    ENDFOREACH
  ENDFOREACH
  save, residual, file = 'F160W_residual.sav'  
END

        
