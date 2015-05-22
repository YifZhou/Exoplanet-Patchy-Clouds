FUNCTION maskoutdq, dq, flagList=flaglist
  IF N_elements(flagList) EQ 0 THEN flagList = [8, 32, 512]
  dq = long(dq)
  mask = dq-dq+1 ;;initialize mask
  FOR k=0, n_elements(flagList) - 1 DO BEGIN
     mask = mask * (1- dq/flagList[k] MOD 2)
  ENDFOR 
  return, mask
END

FUNCTION residual, im, psf, mask, weight = weight
  IF N_elements(weight) EQ 0 THEN weight = im - im + 1
  amp = total(mask*weight*im*psf)/total((mask*weight*psf^2))
  res = total(mask * (weight*(im - psf*amp))^2)/total(mask)
  return, [amp, sqrt(res)]
END

FUNCTION resGrid, im, psf0, err, mask, gc, gridsize
  dxy0 = [13, 13] - gc
  ngrid = 5
  mask00 = make_mask(mask,[[17, 9, 0, 3], [13, 13, 12, 100]])
  grid = fltarr(ngrid, ngrid)
  gridx = gc[0] + (findgen(ngrid) - ngrid/2) * gridSize/float(ngrid/2)
  gridy = gc[1] + (findgen(ngrid) - ngrid/2) * gridSize/float(ngrid/2)

  PSF_core = [[0.0007, 0.025,  0.0007],$
              [0.025,  0.897,  0.025],$
              [0.0007, 0.025, 0.0007]] ;; diffusion convolusion core
  FOR i=0,ngrid-1 DO BEGIN
     FOR j=0,ngrid-1 DO BEGIN
        
        psf = resample(fshift(psf0, -(13-gridx[i])*10, -(13-gridy[j])*10), 27, 27)
        psf = convol(psf, PSF_core)
        optPara = residual(im, psf, mask00, weight = 1/err^2)
        grid[i, j] = optPara[1]
     ENDFOR
  ENDFOR
  gridid = (where(grid EQ min(grid)))[0]
  gridc = [0.0, 0.0]
  gridc[1] = gridid/ngrid
  gridc[0] = gridid MOD ngrid
  newGC = (gridc * gridSize/float(ngrid/2)) + gc - gridsize
  diff = newGC - gc
  newPSF = convol(resample(fshift(psf0, -(13-newGC[0])*10, -(13-newGC[1])*10), 27, 27), PSF_core)
  optPara = residual(im, newPSf, mask00)
  newPSF = newPSF*optPara[0]
  return, diff
END

FUNCTION plotComp, im, psf0
  p=plot(im[*,11],'r+', /stairstep, layout = [5,2,1],/ylog)
  p=plot(psf0[*,11],'b', /stairstep, layout = [5,2,1], /current,/overplot,/ylog)
  p=plot(im[*,12],'r+', /stairstep, layout = [5,2,2], /current,/ylog)
  p=plot(psf0[*,12],'b', /stairstep, layout = [5,2,2], /current,/overplot,/ylog)
  p=plot(im[*,13],'r+', /stairstep, layout = [5,2,3], /current)
  p=plot(psf0[*,13],'b', /stairstep, layout = [5,2,3], /current,/overplot,/ylog )
  p=plot(im[*,14],'r', /stairstep, layout = [5,2,4], /current)
  p=plot(psf0[*,14],'b', /stairstep, layout = [5,2,4], /current,/overplot,/ylog )
  p=plot(im[*,15],'r', /stairstep, layout = [5,2,5], /current)
  p=plot(psf0[*,15],'b', /stairstep, layout = [5,2,5], /current,/overplot,/ylog )
  p=plot(im[11,*],'r', /stairstep, layout = [5,2,6], /current)
  p=plot(psf0[11,*],'b', /stairstep, layout = [5,2,6], /current,/overplot,/ylog )
  p=plot(im[12,*],'r', /stairstep, layout = [5,2,7], /current)
  p=plot(psf0[12,*],'b', /stairstep, layout = [5,2,7], /current,/overplot,/ylog )
  p=plot(im[13,*],'r', /stairstep, layout = [5,2,8], /current)
  p=plot(psf0[13,*],'b', /stairstep, layout = [5,2,8], /current,/overplot,/ylog )
  p=plot(im[14,*],'r', /stairstep, layout = [5,2,9], /current)
  p=plot(psf0[14,*],'b', /stairstep, layout = [5,2,9], /current,/overplot,/ylog )
  p=plot(im[15,*],'r', /stairstep, layout = [5,2,10], /current)
  p=plot(psf0[15,*],'b', /stairstep, layout = [5,2,10], /current,/overplot,/ylog )
  return, p
END


PRO tinytimPSF
  xy0 = [142, 159] ;;; the precise peak position for PSF
  im = mrdfits('icdg02aeq_flt.fits', 1)
  im = im[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  err = mrdfits('icdg02aeq_flt.fits', 2)
  err = err[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  dq = mrdfits('icdg02aeq_flt.fits', 3)
  dq = dq[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  xy0 = [13, 13]
  readcol,'fn.dat', PSF_fn, format = 'a'
  amp = fltarr(N_elements(PSF_fn))
  res = fltarr(N_elements(PSF_fn))
  jitx = fltarr(N_elements(PSF_fn))
  jity = fltarr(N_elements(PSF_fn))
  dis = fltarr(N_elements(PSF_fn))
  PSFList = fltarr(27, 27, N_elements(PSF_fn))
  mask = maskoutdq(dq)
  fixpix, im, mask, im_fixed
  xy = findpeak(im_fixed, 13, 13, range=5)
  print, xy
  for i=0, N_elements(PSF_fn) - 1 DO BEGIN 
     psf0 = mrdfits('./PSF2/'+PSF_fn[i],/silent)
     psf0 = psf0[1:270, 1:270]
     dxy0 = xy0 - xy
     gridSize = 0.4
     WHILE gridsize GT 5*1e-4 DO BEGIN
        diff = resGrid(im, psf0, err, mask, xy, gridSize)
        xy = xy + diff
        gridSize = max([max(abs(diff)) * 2, gridSize/2])
     ENDWHILE
     dxy = xy0 - xy
     
     psf = resample(fshift(psf0, -dxy[0]*10, -dxy[1]*10), 27, 27)
     PSF_core = [[0.0007, 0.025,  0.0007],$
              [0.025,  0.897,  0.025],$
              [0.0007, 0.025, 0.0007]] ;; diffusion convolusion core
     psf = convol(psf, PSF_core)
     mask0 = make_mask(mask, [[13 - dxy[0], 13 - dxy[1], 0, 3], [17, 9, 0, 3], [13-dxy[0], 13-dxy[1], 12, 100]])
     opt_paras = residual(im, psf, mask0, weight = 1/err^2)
     amp[i] = opt_paras[0]
     res[i] = opt_paras[1]
     jitx[i] = float(strmid(PSF_fn[i], 5, 2))
     jity[i] = float(strmid(PSF_fn[i], 13, 2))
     dis[i] = float(strmid(PSF_fn[i], 20, 4))
     print,'PSF name: ', PSF_fn[i]
     print,'opimized rms residual: ', res[i]
     PSFList[*, *, i] = psf
  ENDFOR
  minID = (where(res EQ min(res)))[0]
  psf0 = psfLIST[*,*,minID] * amp[minID]
  fig = plotComp(im, psf0)
  s = surface(im - psf0)
  stop
END
