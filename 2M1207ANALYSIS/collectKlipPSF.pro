FUNCTION maskoutdq, dq, flagList=flaglist
  
  ;;; caculate the mask using data quality array. to exclude certain
  ;;; pixels.
  ;;; the default flags to exclude are:
  ;;; flat 4, 32, and 512
  IF N_elements(flagList) EQ 0 THEN flagList = [4, 32, 512]
  dq = long(dq)
  mask = dq-dq+1 ;;initialize mask as a zero array
  FOR k=0, n_elements(flagList) - 1 DO BEGIN
     mask = mask * (1- dq/flagList[k] MOD 2) ;;; mask out each flags, if (dq/flag) mod 2 == 1,
                                             ;;; then that dq value contains the flag     
  ENDFOR 
  return, mask
END

PRO collectKlipPSF
  ;; collect PSF library FOR klip
  ;; only use 2MASS1207A, since the spectral type OF the background star is unkown
  ;; shift the star image so that the center OF the primary star image
  ;; is located at pixel center
  ;;;; F125W
  df = myreadcsv('2015_Jun_17TinyTimF125Result.csv',$
                 ['FILENAME', 'FILTER', 'ORBIT', 'POSANGLE', 'DITHER', 'EXPOSURESET',$
                  'OBSDATE', 'OBSTIME', 'EXPOTIME', 'FLUXA', 'FLUXB', 'SKY',$
                  'PRIMARY_X', 'PRIMARY_Y', 'SECONDARY_X', 'SECONDARY_Y'])
  dataDIR = '../data/2M1207B/'
  angle0ID = where(df.posangle EQ 0)
  angle1ID = where(df.posangle EQ 1)                ;; save two angle seperately
  angle0cube = fltarr(27, 27, n_elements(angle0ID)) ;; PSFs are 27*27 sub images (3x3 arcsec)
  angle1cube = fltarr(27, 27, n_elements(angle1ID))
  FOR i=0, n_elements(angle0ID) - 1 DO BEGIN
     id = angle0ID(i)
     im = mrdfits(dataDIR + df.filename[id], 1, /silent)
     dq = mrdfits(dataDIR + df.filename[id], 3, /silent)
     mask = maskoutdq(dq)
     cx = df.primary_x[id]
     cy = df.primary_y[id]
     dx = cx - round(cx)
     dy = cy - round(cy)
     subim = im[round(cx) - 14: round(cx) + 14, round(cy) - 14: round(cy) + 14]                       ;; a 29*29 subarray, to avoid the edge effect caused by shifting the image
     fixpix, subim, mask[round(cx) - 14: round(cx) + 14, round(cy) - 14: round(cy) + 14], subim_fixed ;; remove bad pixels, to avoid weird behavior of hot pixel in shifting
     subim = my_shift2d(subim, -dx, -dy, /cubic)
     angle0cube[*, *, i] = subim[1:27, 1:27]
  ENDFOR

  FOR i=0, n_elements(angle1ID) - 1 DO BEGIN
     id = angle1ID(i)
     im = mrdfits(dataDIR + df.filename[id], 1, /silent)
     dq = mrdfits(dataDIR + df.filename[id], 3, /silent)
     mask = maskoutdq(dq)
     cx = df.primary_x[id]
     cy = df.primary_y[id]
     dx = cx - round(cx)
     dy = cy - round(cy)
     subim = im[round(cx) - 14: round(cx) + 14, round(cy) - 14: round(cy) + 14]                       ;; a 29*29 subarray, to avoid the edge effect caused by shifting the image
     fixpix, subim, mask[round(cx) - 14: round(cx) + 14, round(cy) - 14: round(cy) + 14], subim_fixed ;; remove bad pixels, to avoid weird behavior of hot pixel in shifting
     subim = my_shift2d(subim, -dx, -dy, /cubic)
     angle1cube[*, *, i] = subim[1:27, 1:27]
  ENDFOR
  save, angle0cube, angle1cube, file = 'F125W_KLIP_PSF_library.sav'
  
  ;;; F160W
  df = myreadcsv('2015_Jun_17TinyTimF160Result.csv',$
                 ['FILENAME', 'FILTER', 'ORBIT', 'POSANGLE', 'DITHER', 'EXPOSURESET',$
                  'OBSDATE', 'OBSTIME', 'EXPOTIME', 'FLUXA', 'FLUXB', 'SKY',$
                  'PRIMARY_X', 'PRIMARY_Y', 'SECONDARY_X', 'SECONDARY_Y'])
  dataDIR = '../data/2M1207B/'
  angle0ID = where(df.posangle EQ 0)
  angle1ID = where(df.posangle EQ 1)                ;; save two angle seperately
  angle0cube = fltarr(27, 27, n_elements(angle0ID)) ;; PSFs are 27*27 sub images (3x3 arcsec)
  angle1cube = fltarr(27, 27, n_elements(angle1ID))
  FOR i=0, n_elements(angle0ID) - 1 DO BEGIN
     id = angle0ID(i)
     im = mrdfits(dataDIR + df.filename[id], 1, /silent)
     dq = mrdfits(dataDIR + df.filename[id], 3, /silent)
     mask = maskoutdq(dq)
     cx = df.primary_x[id]
     cy = df.primary_y[id]
     dx = cx - round(cx)
     dy = cy - round(cy)
     subim = im[round(cx) - 14: round(cx) + 14, round(cy) - 14: round(cy) + 14]                       ;; a 29*29 subarray, to avoid the edge effect caused by shifting the image
     fixpix, subim, mask[round(cx) - 14: round(cx) + 14, round(cy) - 14: round(cy) + 14], subim_fixed ;; remove bad pixels, to avoid weird behavior of hot pixel in shifting
     subim = my_shift2d(subim, -dx, -dy, /cubic)
     angle0cube[*, *, i] = subim[1:27, 1:27]
  ENDFOR

  FOR i=0, n_elements(angle1ID) - 1 DO BEGIN
     id = angle1ID(i)
     im = mrdfits(dataDIR + df.filename[id], 1, /silent)
     dq = mrdfits(dataDIR + df.filename[id], 3, /silent)
     mask = maskoutdq(dq)
     cx = df.primary_x[id]
     cy = df.primary_y[id]
     dx = cx - round(cx)
     dy = cy - round(cy)
     subim = im[round(cx) - 14: round(cx) + 14, round(cy) - 14: round(cy) + 14]                       ;; a 29*29 subarray, to avoid the edge effect caused by shifting the image
     fixpix, subim, mask[round(cx) - 14: round(cx) + 14, round(cy) - 14: round(cy) + 14], subim_fixed ;; remove bad pixels, to avoid weird behavior of hot pixel in shifting
     subim = my_shift2d(subim, -dx, -dy, /cubic)
     angle1cube[*, *, i] = subim[1:27, 1:27]
  ENDFOR
  save, angle0cube, angle1cube, file = 'F160W_KLIP_PSF_library.sav'
END
