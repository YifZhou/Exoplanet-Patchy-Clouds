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

FUNCTION shiftPSF, psf0, dx, dy, factor = factor
  IF N_elements(factor) EQ 0 THEN factor = 10
  size0 = (size(psf0))[1]
  PSF_core = [[0.0007, 0.025,  0.0007],$
              [0.025,  0.897,  0.025],$
              [0.0007, 0.025, 0.0007]] ;; diffusion convolusion core
  psf = resample(fshift(psf0, dx*factor, dy*factor), size0/factor, size0/factor)
  psf = convol(psf, PSF_core)
  return, psf
END


FUNCTION registerPSF, im, psf0, err, mask, gc
  ;; register psf AND image by minizing the residual
  ;; return the center of the image
  ;; center of resampled psf is always at [13, 13]
  dxy0 = [13, 13] - gc
  ngrid = 5
  grid = fltarr(ngrid, ngrid)  
  gridSize = 0.4
  WHILE gridsize GT 5*1e-4 DO BEGIN
     gridx = gc[0] + (findgen(ngrid) - ngrid/2) * gridSize/float(ngrid/2)
     gridy = gc[1] + (findgen(ngrid) - ngrid/2) * gridSize/float(ngrid/2)
     FOR i=0,ngrid-1 DO BEGIN
        FOR j=0,ngrid-1 DO BEGIN
           psf = shiftPSF(psf0, (13-gridx[i]), (13-gridy[j]), factor = 10)
           optPara = residual(im, psf, mask, weight = 1/err^2)
           grid[i, j] = optPara[1]
        ENDFOR
     ENDFOR
     gridid = (where(grid EQ min(grid)))[0]
     gridc = [0.0, 0.0]
     gridc[1] = gridid/ngrid
     gridc[0] = gridid MOD ngrid
     newGC = [gridx[gridc[0]], gridy[gridc[1]]]
     diff = newGC - gc
     gc = newGC
     gridSize = max([max(abs(diff)) * 2, gridSize/2])
  ENDWHILE
  return, newGC
END

FUNCTION plotComp, im, psf0
  p=plot(im[*,11],'r+', /stairstep, layout = [5,2,1],/ylog)
  p=plot(psf0[*,11],'b', /stairstep, layout = [5,2,1], /current,/overplot,/ylog)
  p=plot(im[*,12],'r+', /stairstep, layout = [5,2,2], /current,/ylog)
  p=plot(psf0[*,12],'b', /stairstep, layout = [5,2,2], /current,/overplot,/ylog)
  p=plot(im[*,13],'r+', /stairstep, layout = [5,2,3], /current,/ylog)
  p=plot(psf0[*,13],'b', /stairstep, layout = [5,2,3], /current,/overplot,/ylog)
  p=plot(im[*,14],'r+', /stairstep, layout = [5,2,4], /current,/ylog)
  p=plot(psf0[*,14],'b', /stairstep, layout = [5,2,4], /current,/overplot,/ylog)
  p=plot(im[*,15],'r+', /stairstep, layout = [5,2,5], /current,/ylog)
  p=plot(psf0[*,15],'b', /stairstep, layout = [5,2,5], /current,/overplot,/ylog)
  p=plot(im[11,*],'r+', /stairstep, layout = [5,2,6],/current, /ylog)
  p=plot(psf0[11,*],'b', /stairstep, layout = [5,2,6], /current,/overplot,/ylog)
  p=plot(im[12,*],'r+', /stairstep, layout = [5,2,7], /current,/ylog)
  p=plot(psf0[12,*],'b', /stairstep, layout = [5,2,7], /current,/overplot,/ylog)
  p=plot(im[13,*],'r+', /stairstep, layout = [5,2,8], /current,/ylog)
  p=plot(psf0[13,*],'b', /stairstep, layout = [5,2,8], /current,/overplot,/ylog)
  p=plot(im[14,*],'r+', /stairstep, layout = [5,2,9], /current,/ylog)
  p=plot(psf0[14,*],'b', /stairstep, layout = [5,2,9], /current,/overplot,/ylog)
  p=plot(im[15,*],'r+', /stairstep, layout = [5,2,10], /current,/ylog)
  p=plot(psf0[15,*],'b', /stairstep, layout = [5,2,10], /current,/overplot,/ylog)
  return, p
END


PRO tinytimPSF
  xy0 = [135, 161] ;;; the precise peak position for PSF
  im = mrdfits('icdg01zeq_flt.fits', 1)
  im = im[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  err = mrdfits('icdg01zeq_flt.fits', 2)
  err = err[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  dq = mrdfits('icdg01zeq_flt.fits', 3)
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
     psf0 = mrdfits('./PSFs/'+PSF_fn[i],/silent)
     psf0 = psf0[1:270, 1:270]
     mask1 = make_mask(mask,[[17, 9, 0, 3], [13, 13, 11, 100]])
     xy = registerPSF(im, psf0, err, mask1, xy)
     dxy = xy - [13, 13]
     psf = shiftPSF(psf0, -dxy[0], -dxy[1], factor = 10)
     mask2 = make_mask(mask, [[13 - dxy[0], 13 - dxy[1], 0, 3], [17, 9, 0, 3], [13-dxy[0], 13-dxy[1], 12, 100]])
     opt_paras = residual(im, psf, mask2, weight = 1/err^2)
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
  im_subbed = im - psf0
  comp_xy = [18, 10] ;; for angle1 at first gc position, the coordinate of companion object is [18, 10]
  mask3 = mask
  mask3 = fltarr(27, 27)
  mask3[comp_xy[0]-1:comp_xy[0]+1, comp_xy[1]-1:comp_xy[1]+1] = 1 ;; only use the center 9 pixel to locate the companion obj
  comp_xy = registerPSF(im_subbed, PSFList[*,*,minID], err, mask3, [18, 10])
  
  stop
END
