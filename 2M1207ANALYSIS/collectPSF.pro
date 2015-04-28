PRO collectPSF, infoFile, output
  dataDIR = '../data/2M1207B/'
  fileInfo = myReadCSV(infoFile, ['filename', 'filter', 'orbit', 'posang', 'dither', 'exposure_set','obs_date','obs_time','exposure_time'])
  ;;get the dither pattern,
  ;; dither = 0: (0, 0)
  ;; dither = 1: (1, 0)
  ;; dither = 2: (0, 1)
  ;; dither = 3: (1, 1)
  fileInfo = add_tag(fileInfo, 'ditherX', fileInfo.dither MOD 2)
  fileInfo = add_tag(fileInfo, 'ditherY', fileInfo.dither/2)
  
  ;;primary and the bright background star positon on dither = 0 image
  ;;at two different roll angle
  primaryPos1 = [145.0, 172.7]
  bkStarPos1 = [194.9, 134.4]
  primaryPos2 = [141.7, 159.1]
  bkStarPos2 = [172.5, 100.9]

  id125 = where(fileInfo.filter EQ 'F125W')
  id160 = where(fileInfo.filter EQ 'F160W')
  n125 = N_elements(id125)
  n160 = N_elements(id160)

  image = {rollAngle:0.0, x0:0, y0:0.0, image:fltarr(51, 51), dq:fltarr(51, 51), err:fltarr(51, 51)}
  PSF = {rollAngle:0.0, image:fltarr(51, 51), dq:fltarr(51, 51), err:fltarr(51, 51)}
  image125 = replicate(image, n125)
  image160 = replicate(image, n160)
  PSF125 = replicate(PSF, n125*2)
  PSF160 = replicate(PSF, n160*2)
  
  FOR i = 0, n125-1 DO BEGIN
     im = mrdfits(dataDIR + fileInfo.filename[id125[i]], 1)
     err = mrdfits(dataDIR + fileInfo.filename[id125[i]], 2)
     dq = mrdfits(dataDIR + fileInfo.filename[id125[i]], 3)
     IF fileInfo.posang[id125[i]] EQ 202 THEN BEGIN
        cStar = findpeak(im, primaryPos1[0] + fileInfo.ditherX[id125[i]]$
                         , primaryPos1[1] + fileInfo.ditherY[id125[i]])
        cbkStar = findpeak(im, bkStarPos1[0] + fileInfo.ditherX[id125[i]]$
                           , bkStarPos1[1] + fileInfo.ditherY[id125[i]])
     ENDIF ELSE BEGIN
        cStar = findpeak(im, primaryPos2[0] + fileInfo.ditherX[id125[i]]$
                         , primaryPos2[1] + fileInfo.ditherY[id125[i]])
        cbkStar = findpeak(im, bkStarPos2[0] + fileInfo.ditherX[id125[i]]$
                           , bkStarPos2[1] + fileInfo.ditherY[id125[i]])
     ENDELSE 
        image125[i].image = im[floor(cStar[0]) -25: floor(cStar[0]) + 25, floor(cStar[1]) -25: floor(cStar[1]) + 25]
        image125[i].rollAngle = fileInfo.posang[id125[i]]
        image125[i].x0 = floor(cStar[0])
        image125[i].y0 = floor(cStar[1])
        image125[i].dq = dq[floor(cStar[0]) -25: floor(cStar[0]) + 25, floor(cStar[1]) -25: floor(cStar[1]) + 25]
        image125[i].err = err[floor(cStar[0]) -25: floor(cStar[0]) + 25, floor(cStar[1]) -25: floor(cStar[1]) + 25]
        PSF125[2*i].rollAngle = fileInfo.posang[id125[i]]
        PSF125[2*i+1].rollAngle = 0
        PSF125[2*i].image = im[floor(cStar[0]) -25: floor(cStar[0]) + 25, floor(cStar[1]) -25: floor(cStar[1]) + 25]
        PSF125[2*i+1].image = im[floor(cbkStar[0]) -25: floor(cbkStar[0]) + 25, floor(cbkStar[1]) -25: floor(cbkStar[1]) + 25]
        PSF125[2*i].dq = dq[floor(cStar[0]) -25: floor(cStar[0]) + 25, floor(cStar[1]) -25: floor(cStar[1]) + 25]
        PSF125[2*i+1].dq = dq[floor(cbkStar[0]) -25: floor(cbkStar[0]) + 25, floor(cbkStar[1]) -25: floor(cbkStar[1]) + 25]
        PSF125[2*i].err = err[floor(cStar[0]) -25: floor(cStar[0]) + 25, floor(cStar[1]) -25: floor(cStar[1]) + 25]
        PSF125[2*i+1].err = err[floor(cbkStar[0]) -25: floor(cbkStar[0]) + 25, floor(cbkStar[1]) -25: floor(cbkStar[1]) + 25]
     ENDFOR
  
    FOR i = 0, n160-1 DO BEGIN
     im = mrdfits(dataDIR + fileInfo.filename[id160[i]], 1)
     err = mrdfits(dataDIR + fileInfo.filename[id160[i]], 2)
     dq = mrdfits(dataDIR + fileInfo.filename[id160[i]], 3)
     IF fileInfo.posang[id160[i]] EQ 202 THEN BEGIN
        cStar = findpeak(im, primaryPos1[0] + fileInfo.ditherX[id160[i]]$
                         , primaryPos1[1] + fileInfo.ditherY[id160[i]])
        cbkStar = findpeak(im, bkStarPos1[0] + fileInfo.ditherX[id160[i]]$
                           , bkStarPos1[1] + fileInfo.ditherY[id160[i]])
     ENDIF ELSE BEGIN
        cStar = findpeak(im, primaryPos2[0] + fileInfo.ditherX[id160[i]]$
                         , primaryPos2[1] + fileInfo.ditherY[id160[i]])
        cbkStar = findpeak(im, bkStarPos2[0] + fileInfo.ditherX[id160[i]]$
                           , bkStarPos2[1] + fileInfo.ditherY[id160[i]])
     ENDELSE 
        image160[i].image = im[floor(cStar[0]) -25: floor(cStar[0]) + 25, floor(cStar[1]) -25: floor(cStar[1]) + 25]
        image160[i].rollAngle = fileInfo.posang[id160[i]]
        image160[i].x0 = floor(cStar[0])
        image160[i].y0 = floor(cStar[1])
        image160[i].dq = dq[floor(cStar[0]) -25: floor(cStar[0]) + 25, floor(cStar[1]) -25: floor(cStar[1]) + 25]
        image160[i].err = err[floor(cStar[0]) -25: floor(cStar[0]) + 25, floor(cStar[1]) -25: floor(cStar[1]) + 25]
        PSF160[2*i].rollAngle = fileInfo.posang[id160[i]]
        PSF160[2*i+1].rollAngle = 0
        PSF160[2*i].image = im[floor(cStar[0]) -25: floor(cStar[0]) + 25, floor(cStar[1]) -25: floor(cStar[1]) + 25]
        PSF160[2*i+1].image = im[floor(cbkStar[0]) -25: floor(cbkStar[0]) + 25, floor(cbkStar[1]) -25: floor(cbkStar[1]) + 25]
        PSF160[2*i].dq = dq[floor(cStar[0]) -25: floor(cStar[0]) + 25, floor(cStar[1]) -25: floor(cStar[1]) + 25]
        PSF160[2*i+1].dq = dq[floor(cbkStar[0]) -25: floor(cbkStar[0]) + 25, floor(cbkStar[1]) -25: floor(cbkStar[1]) + 25]
        PSF160[2*i].err = err[floor(cStar[0]) -25: floor(cStar[0]) + 25, floor(cStar[1]) -25: floor(cStar[1]) + 25]
        PSF160[2*i+1].err = err[floor(cbkStar[0]) -25: floor(cbkStar[0]) + 25, floor(cbkStar[1]) -25: floor(cbkStar[1]) + 25]
     ENDFOR
    save, image125, PSF125, filename = output + '_F125W.sav'
    save, image160, PSF160, filename = output + '_F160W.sav'
END

