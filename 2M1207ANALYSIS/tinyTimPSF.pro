FUNCTION maskoutdq, dq, flagList=flaglist
  IF N_elements(flagList) EQ 0 THEN flagList = [8, 32, 512]
  dq = long(dq)
  mask = dq-dq+1 ;;initialize mask
  FOR k=0, n_elements(flagList) - 1 DO BEGIN
     mask = mask * (1- dq/flagList[k] MOD 2)
  ENDFOR 
  return, mask
END

FUNCTION residual, im, psf, mask
  amp = total(mask*im * psf)/total((mask * psf^2))
  res = total(mask * (im - psf*amp)^2)/total(mask)
  return, [amp, sqrt(res)]
END

FUNCTION resGrid, im, psf0, mask, gc, gridsize
  dxy0 = [13, 13] - gc
  ngrid = 5
  mask00 = make_mask(mask,[[17, 9, 0, 3], [13, 13, 12, 100]])
  grid = fltarr(ngrid, ngrid)
  gridx = gc[0] + (findgen(ngrid) - 3) * gridSize/float(ngrid/2)
  gridy = gc[1] + (findgen(ngrid) - 3) * gridSize/float(ngrid/2)

  FOR i=0,6 DO BEGIN
     FOR j=0,6 DO BEGIN
        
        psf = resample(fshift(psf0, -(13-gridx[i])*10, -(13-gridy[j])*10), 27, 27)
        optPara = residual(im, psf, mask00)
        grid[i, j] = optPara[1]
     ENDFOR
  ENDFOR
  gridid = (where(grid EQ min(grid)))[0]
  gridc = [0.0, 0.0]
  gridc[1] = gridid/ngrid
  gridc[0] = gridid MOD ngrid
  newGC = (gridc * gridSize/float(ngrid/2)) + gc - gridsize
  diff = newGC - gc
  ;;print, 'min res = ', min(grid)
  return, diff
END



PRO tinytimPSF
  xy0 = [136, 162] ;;; the precise peak position for PSF
  im = mrdfits('icdg01zeq_flt.fits', 1)
  im = im[136-13:136+13, 162-13:162+13]
  err = mrdfits('icdg01zeq_flt.fits', 2)
  err = err[136-13:136+13, 162-13:162+13]
  dq = mrdfits('icdg01zeq_flt.fits', 3)
  dq = dq[136-13:136+13, 162-13:162+13]
  xy0 = [13, 13]
  ;; PSF_fn = ['Jitx_0_Jity_0_Dis_3.00_00.fits','Jitx_10_Jity_0_Dis_3.00_00.fits',$
  ;;           'Jitx_20_Jity_0_Dis_3.00_00.fits', 'Jitx_30_Jity_0_Dis_3.00_00.fits', $
  ;;           'Jitx_0_Jity_10_Dis_3.00_00.fits','Jitx_10_Jity_10_Dis_3.00_00.fits',$
  ;;           'Jitx_20_Jity_10_Dis_3.00_00.fits','Jitx_30_Jity_10_Dis_3.00_00.fits',$
  ;;           'Jitx_0_Jity_20_Dis_3.00_00.fits','Jitx_10_Jity_20_Dis_3.00_00.fits',$
  ;;           'Jitx_20_Jity_20_Dis_3.00_00.fits',	'Jitx_30_Jity_20_Dis_3.00_00.fits',$
  ;;           'Jitx_0_Jity_30_Dis_3.00_00.fits', 'Jitx_10_Jity_30_Dis_3.00_00.fits', $
  ;;           'Jitx_20_Jity_30_Dis_3.00_00.fits','Jitx_30_Jity_30_Dis_3.00_00.fits']

  readcol,'fn.dat', PSF_fn, format = 'a'
  amp = fltarr(N_elements(PSF_fn))
  res = fltarr(N_elements(PSF_fn))
  jitx = fltarr(N_elements(PSF_fn))
  jity = fltarr(N_elements(PSF_fn))
  dis = fltarr(N_elements(PSF_fn))
  PSFList = fltarr(27, 27, N_elements(PSF_fn))
  mask = maskoutdq(dq)
  fixpix, im, mask, im_fixedn
  xy = findpeak(im_fixed, 13, 13, range=5)
  print, xy
  for i=0, N_elements(PSF_fn) - 1 DO BEGIN 
     psf0 = mrdfits('./PSFs/'+PSF_fn[i],/silent)
     psf0 = psf0[1:270, 1:270]
     dxy0 = xy0 - xy
     mask0 = make_mask(mask, [17, 9, 0, 3])
     mask00 = make_mask(mask, [[13 - dxy0[0], 13 - dxy0[1], 0, 3], [17, 9, 0, 3], [13-dxy0[0], 13-dxy0[1], 12, 100]])
     gridSize = 0.2
     WHILE gridsize GT 5*1e-4 DO BEGIN
        diff = resGrid(im, psf0, mask, xy, gridSize)
        xy = xy + diff
        gridSize = max([max(abs(diff)) * 5, gridSize/2])
     ENDWHILE     
     dxy = xy0 - xy
     psf = resample(fshift(psf0, -dxy[0]*10, -dxy[1]*10), 27, 27)
     mask0 = make_mask(mask, [[13 - dxy[0], 13 - dxy[1], 0, 3], [17, 9, 0, 3], [13-dxy[0], 13-dxy[1], 12, 100]])
     opt_paras = residual(im, psf, mask0)
     amp[i] = opt_paras[0]
     res[i] = opt_paras[1]
     jitx[i] = float(strmid(PSF_fn[i], 5, 2))
     jity[i] = float(strmid(PSF_fn[i], 13, 2))
     dis[i] = float(strmid(PSF_fn[i], 20, 4))
     print,'opimized rms residual: ', res[i]
     PSFList[*, *, i] = psf
  ENDFOR
  minID = (where(res EQ min(res)))[0]
  psf0 = psfLIST[*,*,minID] * amp[minID]
  x = 6+findgen(15)
  p=plot(x, im[6:20,11],'r+', /stairstep, layout = [3,2,1])
  p=plot(x, psf0[6:20,11],'b', /stairstep, layout = [3,2,1], /current, /overplot)
  p=plot(x, im[6:20,12],'r+', /stairstep, layout = [3,2,2], /current)
  p=plot(x, psf0[6:20,12],'b', /stairstep, layout = [3,2,2], /current, /overplot)
  p=plot(x, im[6:20,13],'r+', /stairstep, layout = [3,2,3], /current)
  p=plot(x, psf0[6:20,13],'b', /stairstep, layout = [3,2,3], /current, /overplot)
  p=plot(x, im[11,6:20],'r+', /stairstep, layout = [3,2,4],/current)
  p=plot(x, psf0[11,6:20],'b', /stairstep, layout = [3,2,4], /current, /overplot)
  p=plot(x, im[12,6:20],'r+', /stairstep, layout = [3,2,5], /current)
  p=plot(x, psf0[12,6:20],'b', /stairstep, layout = [3,2,5], /current, /overplot)
  p=plot(x, im[13,6:20],'r+', /stairstep, layout = [3,2,6], /current)
  p=plot(x, psf0[13,6:20],'b', /stairstep, layout = [3,2,6], /current, /overplot)
  s = surface(im - psf0)
  stop
END
