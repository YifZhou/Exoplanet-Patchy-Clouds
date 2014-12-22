pro prepData, infoStruct, dataDir, prepFN
  ;; apply no shift to the image
  F125ID = where(fileInfo.filter EQ 'F125W')
  F160ID = where(fileInfo.filter EQ 'F160W')
  im125 = mrdfits(dataDir + infoStruct.filename[F125ID[0]])
  im160 = mrdfits(dataDir + infoStruct.filename[F160ID[0]])
  nFile = N_ELEMENTS(infoStruct.filename)
  xoff = fltarr(nFile)
  yoff = fltarr(nFile)
  cube = MAKE_ARRAY(256, 256, nFile, /DOUBLE) ;; list to save images
  imageSz = 256
  FOR i = 0, nFile -1 DO BEGIN
     im = mrdfits(dataDir + infoStruct.filename[i], 1, header1)
     IF infoStruct.filter[i] EQ 'F125W' THEN im0 = im125 ELSE im0 = im160
     corr = crosscorr(im0, im, pmax, dxy, range = 10)
     xoff[i] = dxy[0]
     yoff[i] = dxy[1]
     cube[*,*, i] = im
     print,'i',' image prepared'
  ENDFOR
  infoStruct = add_tag(infoStruct, xoff, 'xoff')
  infoStruct = add_tag(infoStruct, yoff, 'yoff')
  saveFN = strn(floor(systime(/julian))) + 'prepared.sav'
  save, cube, infoList, filename = saveFN
end


  
