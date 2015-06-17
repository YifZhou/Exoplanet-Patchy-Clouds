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

PRO subtract
  df = myreadcsv('2015_Jun_16TinyTimF125Result.csv',$
                 ['FILENAME', 'FILTER', 'ORBIT', 'POSANGLE', 'DITHER', 'EXPOSURESET',$
                  'OBSDATE', 'OBSTIME', 'EXPOTIME', 'FLUXA', 'FLUXB', 'SKY',$
                  'PRIMARY_X', 'PRIMARY_Y', 'SECONDARY_X', 'SECONDARY_Y'])
  dataDIR = '../data/2M1207B/'
  id0 = (where(df.posangle EQ 0))[0]
  id1 = (where(df.posangle EQ 1))[0]
  im0 = mrdfits(dataDIR + df.filename[id0], 1, /silent)
  err0 = mrdfits(dataDIR + df.filename[id0], 2, /silent)
  dq0 = mrdfits(dataDIR + df.filename[id0], 3, /silent)
  mask0 = maskoutdq(dq0)  
  im1 = mrdfits(dataDIR + df.filename[id1], 1, /silent)
  err1 = mrdfits(dataDIR + df.filename[id1], 2, /silent)
  dq1 = mrdfits(dataDIR + df.filename[id1], 3, /silent)
  mask1 = maskoutdq(dq1)

  cxy0 = [df.primary_x[id0], df.primary_y[id0]]
  cxy1 = [df.primary_x[id1], df.primary_y[id1]]
  intC0 = floor(cxy0) ;; int part of the first image centroid
  fracC0 = cxy0 - intC0 ;; fractional part of the first image centroid
  intC1 = floor(cxy1)  ;; same as previous two lines
  fracC1 = cxy1 - intC1  
  subIm0 = im0[intC0[0]-20:intC0[0]+20, intC0[1]-20:intC0[1]+20]
  subIm1 = im1[intC1[0]-20:intC1[0]+20, intC1[1]-20:intC1[1]+20]
  mask0  = mask0[intC0[0]-20:intC0[0]+20, intC0[1]-20:intC0[1]+20]
  mask1 = mask1[intC1[0]-20:intC1[0]+20, intC1[1]-20:intC1[1]+20]
  fixpix, subim0, mask0, subim0_fixed, /silent
  fixpix, subim1, mask1, subim1_fixed, /silent

  diff = fracC0 - fracC1
  subim0_fixed = my_shift2d(subim0_fixed, -diff[0]/2, -diff[1]/2, /cubic)
  subim1_fixed = my_shift2d(subim1_fixed, diff[0]/2, diff[1]/2, /cubic)
  imdiff = subim0_fixed -subim1_fixed
  print, diff, id0, id1
;  subim2 = fshift(subim2, -dxy[0], -dxy[1])
  ;; c2 = findpeak(subim2, 41*nSamp/2, 41*nSamp/2, range = 3*nSamp)
  ;; print, c1
  ;; subim2 = subim2 * c1[2]/c2[2]
  ;; c2 = findpeak(subim2, 41*nSamp/2, 41*nSamp/2, range = 3*nSamp)
  ;; print, c2
END
