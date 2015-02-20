

PRO makeFLTPSF, infoFile
  ;; generate PSF file FOR flt.fits file
  fileInfo = myReadCSV(infoFile, ['FILENAME', 'FILTER', 'ORBIT', 'POSANG', 'DITHER', 'EXPOSURE_SET','OBS_DATE','OBS_TIME','EXPOSURE_TIME', 'XOFF', 'YOFF'])
  dataDIR = '../data/ABPIC-B_myfits/'
  ID125 = where(fileInfo.filter EQ 'F125W')
  ID160 = where(fileInfo.filter EQ 'F160W')
  PSF = {filter:'', rollAngle:0.0, dither:0, xOff:0.0, yOff:0.0, PSF:fltarr(256,256)}
  PSFList = replicate(PSF, 4)
  FILTER = ['F125W', 'F160W']
  angle = [101.0, 129.0]
  FOR i = 0, 1 DO BEGIN
     FOR  j = 0, 1 DO BEGIN 
           id = where((fileInfo.FILTER EQ FILTER[i]) AND (fileInfo.POSANG EQ angle[j]) )
           PSFcube = fltarr(256, 256, N_elements(id))
           fileList = fileInfo.FILENAME[id]
           xoffList = fileInfo.xOff[id]
           yoffList = fileInfo.yOff[id]
           xoff0 = xoffList[0]
           yoff0 = yoffList[0]
           xoffList = xoffList - xoff0
           yoffList = yoffList - yoff0
           
           PSFList[i*2 + j].filter = filter[i]
           PSFList[i*2 + j].rollAngle = angle[j]
           PSFList[i*2 + j].dither = 0
           PSFList[i*2 + j].xOff = xoff0
           PSFList[i*2 + j].yOff = yoff0
           FOR PSF_i = 0, N_ELEMENTS(id) - 1 DO BEGIN
              im = mrdfits(dataDIR + fileList[PSF_i], 1, hd)
              ;; PSFcube[*, *, PSF_i] = fshift(im, -xoffList[PSF_i], -yoffList[PSF_i])
              ;; print, -xoffList[PSF_i], -yoffList[PSF_i]
              PSFcube[*,*,PSF_i] = im
           ENDFOR
           PSFList[i*2 + j].PSF = median(PSFcube, dimension = 3, /even)
        ENDFOR
     ENDFOR
  save, PSFList, filename = 'myfits_PSF.sav'
END

PRO makeIMAPSF, infoFile
  ;; generate PSF file FOR flt.fits file
  fileInfo = myReadCSV(infoFile, ['FILENAME', 'FILTER', 'ORBIT', 'POSANG', 'DITHER', 'EXPOSURE_SET','OBS_DATE','OBS_TIME','EXPOSURE_TIME', 'XOFF', 'YOFF'])
  dataDIR = '../data/ABPIC-B/'
  ID125 = where(fileInfo.filter EQ 'F125W')
  ID160 = where(fileInfo.filter EQ 'F160W')
  PSF = {filter:'', rollAngle:0.0, dither:0, xOff:0.0, yOff:0.0, PSF:fltarr(266,266)}
  PSFList = replicate(PSF, 16)
  FILTER = ['F125W', 'F160W']
  angle = [101.0, 129.0]
  F125SubRd = [1, 6, 11, 16]
  F160SubRd = [1, 6]
  FOR i = 0, 1 DO BEGIN
     FOR  j = 0, 1 DO BEGIN 
        FOR k = 0, 3 DO BEGIN
           id = where((fileInfo.FILTER EQ FILTER[i]) AND (fileInfo.POSANG EQ angle[j]) AND (fileInfo.DITHER EQ k))
           PSFcube = fltarr(266, 266, N_elements(id))
           fileList = fileInfo.FILENAME[id]
           xoffList = fileInfo.xOff[id]
           yoffList = fileInfo.yOff[id]
           xoff0 = xoffList[0]
           yoff0 = yoffList[0]
           xoffList = xoffList - xoff0
           yoffList = yoffList - yoff0
           PSFList[i * 8 + j * 4 + k].filter = filter[i]
           PSFList[i * 8 + j * 4 + k].rollAngle = angle[j]
           PSFList[i * 8 + j * 4 + k].dither = k
           PSFList[i * 8 + j * 4 + k].xOff = xoff0
           PSFList[i * 8 + j * 4 + k].yOff = yoff0
           FOR PSF_i = 0, N_ELEMENTS(id) - 1 DO BEGIN
              IF i EQ 0 THEN im = readImaFile(dataDIR + fileList[PSF_i], [1, 6, 11, 16])$
                                 ELSE im = readImaFile(dataDIR + fileList[PSF_i], [1, 6])
              ;; PSFcube[*, *, PSF_i] = fshift(im, -xoffList[PSF_i], -yoffList[PSF_i])
              ;; print, -xoffList[PSF_i], -yoffList[PSF_i]
              PSFcube[*,*,PSF_i] = im
           ENDFOR
           PSFList[i * 8 + j * 4 + k].PSF = median(PSFcube, dimension = 3, /even)
        ENDFOR
     ENDFOR
  ENDFOR
  save, PSFList, filename = 'ima_PSF.sav'
END

FUNCTION readImaFile, filename, subReadID
  ;; function to read IMA file
  ;; average combine subreads
  im = fltarr(266, 266)
  FOR i = 0, N_ELEMENTS(subReadID) - 1 DO im = im + mrdfits(filename, subReadID[i])
  return, im/N_elements(subReadID)
END

FUNCTION myReadCSV,fn, tags
  ;; function for reading csv files
  ;; change the names of tags
  strct = read_csv(fn)
  return, rename_tags(strct, ['FIELD01','FIELD02','FIELD03','FIELD04','FIELD05','FIELD06','FIELD07','FIELD08','FIELD09', 'FIELD10', 'FIELD11'], tags)
END