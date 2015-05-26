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

FUNCTION residual, im, psf, mask, weight = weight
  ;;; use least chisq fit to calculate the amplitude of PSF, and
  ;;; return the amplitude and reduced residual
  IF N_elements(weight) EQ 0 THEN weight = im - im + 1 ;;; default value for the weight array is a ones array
  amp = total(mask*weight*im*psf)/total((mask*weight*psf^2))   ;;; calculate the amplitude of the residual by least chisq fit
  res = total(mask * (weight*(im - psf*amp))^2)/total(mask)    ;;; calculate the residual, only use the pixels that are not masked
  return, [amp, sqrt(res)]
END

FUNCTION shiftPSF, psf0, dx, dy, factor = factor
  ;; shift the over-sampled PSF using fshift, which implement bilinear
  ;; interpolation to shift the PSFs. After shift the PSF, resample
  ;; the PSF using the sample rate OF the origial image. Finally,
  ;; convolove the image with a intrapixel diffusion core.
  
  ;; input parameter:
  ;; dx, dy: the shift distance in x AND y direction. The pixel sizes FOR both dx AND dy are the same as the original image, instead OF oversampled PSF
  ;; factor: the oversample rate, default value is 10
  
  IF N_elements(factor) EQ 0 THEN factor = 10
  size0 = (size(psf0))[1]
  PSF_core = [[0.0007, 0.025,  0.0007],$
              [0.025,  0.897,  0.025],$
              [0.0007, 0.025, 0.0007]] ;; intrapixel diffusion core. convol this with the resampled PSF, as indicated by tiny tim manual.
  
  psf = resample(fshift(psf0, dx*factor, dy*factor), size0/factor, size0/factor)
  psf = convol(psf, PSF_core)
  return, psf
END


FUNCTION registerPSF, im, psf0, err, mask, gc
  ;; register psf AND image by minizing the residual
  ;; return the center of the image
  ;; center of resampled psf is always at [13, 13]
  
  ;; in put paramenters:
  ;; im: the original image, center is around [13, 13]
  ;; PSF0: tinytim PSF, 10x oversampled, 270x270 in size, after resampling to wfc3 ir sample rate, center is [13, 13]
  ;; err: error array extracted from fits file, used FOR calculate chisq
  ;; mask: a 0-1 array to indicate which pixel to be masked out. 1 stands FOR transparent AND 0 stands FOR mask
  ;; gc: initial value FOR grid center
  
  dxy0 = [13, 13] - gc
  ngrid = 5 ;;; number of grid on each side
  grid = fltarr(ngrid, ngrid)  ;;; initalize the grid point
  gridSize = 0.4               ;;; inital lize the distance of lence of the grid on each side
                               ;;; the total lence is 2 * gridSize,
                               ;;; which means the grid covers a
                               ;;; square whose edge is gridSize away
                               ;;; from the center
  WHILE gridsize GT 5*1e-4 DO BEGIN
     gridx = gc[0] + (findgen(ngrid) - ngrid/2) * gridSize/float(ngrid/2) ;;; x coordinate of each grid point
     gridy = gc[1] + (findgen(ngrid) - ngrid/2) * gridSize/float(ngrid/2) ;;; y coordinate of each grid point
     FOR i=0,ngrid-1 DO BEGIN
        FOR j=0,ngrid-1 DO BEGIN
           psf = shiftPSF(psf0, (gridx[i]-13), (gridy[j]-13), factor = 10)
           optPara = residual(im, psf, mask, weight = 1/err^2)
           grid[i, j] = optPara[1]
        ENDFOR
     ENDFOR
     gridid = (where(grid EQ min(grid)))[0]
     gridc = [0.0, 0.0]
     gridc[1] = gridid/ngrid
     gridc[0] = gridid MOD ngrid 
     newGC = [gridx[gridc[0]], gridy[gridc[1]]] ;;; find the x and y coordinate of the grid point that has the least residual
     diff = newGC - gc
     gc = newGC   ;;; renew the grid center
     gridSize = max([max(abs(diff)) * 2, gridSize/2])   ;;; renew the gridSize
  ENDWHILE
  return, newGC
END

FUNCTION fit2PSFs, im, err, PSF1, PSF2, mask
  ;;; fit two PSf to one image to calculate the flux of secondary
  ;;; PSF1: PSF of the primary
  ;;; PSF2: PSF of the secondary
  ;;; return the amplitude of two PSFs
  A = [[total(mask*(PSF1^2/err^2)), total(mask*(PSF1*PSF2/err^2))],$
       [total(mask*(PSF1*PSF2/err^2)),total(mask*(PSF2^2/err^2))]]
  b = [[total(mask*(PSF1*im/err^2))], [total(mask*(PSF2*im/err^2))]]
  amp = LA_invert(A) ## b
  return, amp
END


FUNCTION plotComp, im, psf0
  
  ;; plot the slices OF the image profile
  ;; first row is x direction, central 5 pixels
  ;; second row is y direction, central 5 pixels
  ;; red + is the original image
  ;; blue step line is tinytim psfs
  
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

FUNCTION plotFitResult, im, PSF1, PSF2, im_c
  PSF = PSF1 + PSF2
  p=plot(im[im_c[0]-5:im_c[0]+5,im_c[1] - 1],'r+', layout = [3,2,1],/ylog)
  p=plot(PSF1[im_c[0]-5:im_c[0]+5,im_c[1] - 1],'b', /stairstep, layout = [3,2,1], /current,/overplot,/ylog)
  p=plot(PSF2[im_c[0]-5:im_c[0]+5,im_c[1] - 1],'m', /stairstep, layout = [3,2,1], /current,/overplot,/ylog)
  p=plot(PSF[im_c[0]-5:im_c[0]+5,im_c[1] - 1],'g', linewidth = 1.5, /stairstep, layout = [3,2,1], /current,/overplot,/ylog)
  
  p=plot(im[im_c[0]-5:im_c[0]+5,im_c[1]],'r+', layout = [3,2,2], /current, /ylog)
  p=plot(PSF1[im_c[0]-5:im_c[0]+5,im_c[1]],'b', /stairstep, layout = [3,2,2], /current,/overplot,/ylog)
  p=plot(PSF2[im_c[0]-5:im_c[0]+5,im_c[1]],'m', /stairstep, layout = [3,2,2], /current,/overplot,/ylog)
  p=plot(PSF[im_c[0]-5:im_c[0]+5,im_c[1]],'g', linewidth = 1.5, /stairstep, layout = [3,2,2], /current,/overplot,/ylog)

  p=plot(im[im_c[0]-5:im_c[0]+5,im_c[1]+1],'r+', layout = [3,2,3], /current, /ylog)
  p=plot(PSF1[im_c[0]-5:im_c[0]+5,im_c[1]+1],'b', /stairstep, layout = [3,2,3], /current,/overplot,/ylog)
  p=plot(PSF2[im_c[0]-5:im_c[0]+5,im_c[1]+1],'m', /stairstep, layout = [3,2,3], /current,/overplot,/ylog)
  p=plot(PSF[im_c[0]-5:im_c[0]+5,im_c[1]+1],'g', linewidth = 1.5, /stairstep, layout = [3,2,3], /current,/overplot,/ylog)

  p=plot(im[im_c[0]-1, im_c[1]-5:im_c[1]+5],'r+', layout = [3,2,4], /current, /ylog)
  p=plot(PSF1[im_c[0]-1, im_c[1]-5:im_c[1]+5],'b', /stairstep, layout = [3,2,4], /current,/overplot,/ylog)
  p=plot(PSF2[im_c[0]-1, im_c[1]-5:im_c[1]+5],'m', /stairstep, layout = [3,2,4], /current,/overplot,/ylog)
  p=plot(PSF[im_c[0]-1, im_c[1]-5:im_c[1]+5],'g', linewidth = 1.5, /stairstep, layout = [3,2,4], /current,/overplot,/ylog)

  p=plot(im[im_c[0], im_c[1]-5:im_c[1]+5],'r+', layout = [3,2,5], /current, /ylog)
  p=plot(PSF1[im_c[0], im_c[1]-5:im_c[1]+5],'b', /stairstep, layout = [3,2,5], /current,/overplot,/ylog)
  p=plot(PSF2[im_c[0], im_c[1]-5:im_c[1]+5],'m', /stairstep, layout = [3,2,5], /current,/overplot,/ylog)
  p=plot(PSF[im_c[0], im_c[1]-5:im_c[1]+5],'g', linewidth = 1.5, /stairstep, layout = [3,2,5], /current,/overplot,/ylog)
 
  p=plot(im[im_c[0]+1, im_c[1]-5:im_c[1]+5],'r+', layout = [3,2,6], /current, /ylog)
  p=plot(PSF1[im_c[0]+1, im_c[1]-5:im_c[1]+5],'b', /stairstep, layout = [3,2,6], /current,/overplot,/ylog)
  p=plot(PSF2[im_c[0]+1, im_c[1]-5:im_c[1]+5],'m', /stairstep, layout = [3,2,6], /current,/overplot,/ylog)
  p=plot(PSF[im_c[0]+1, im_c[1]-5:im_c[1]+5],'g', linewidth = 1.5, /stairstep, layout = [3,2,6], /current,/overplot,/ylog)
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
  readcol,'./PSF/angle_0_dither_0/fn.dat', PSF_fn, format = 'a'
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
     psf0 = mrdfits('./PSF/angle_0_dither_0/'+PSF_fn[i],/silent)
     psf0 = psf0[1:270, 1:270]
     mask1 = make_mask(mask,[[17, 9, 0, 3], [13, 13, 11, 100]])
     xy = registerPSF(im, psf0, err, mask1, xy)
     dxy = xy - [13, 13] ;; the displacement of the center of the image to the center of the psf
     psf = shiftPSF(psf0, dxy[0], dxy[1], factor = 10)
     mask2 = make_mask(mask, [[xy[0], xy[1], 0, 3], [17, 9, 0, 3], [xy[0], xy[1], 12, 100]])
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
  im_subbed = im - psfLIST[*,*,minID] * amp[minID]
  comp_xy = [18, 10] ;; for angle1 at first gc position, the coordinate of companion object is [18, 10]
  mask3 = mask
  mask3 = fltarr(27, 27)
  mask3[comp_xy[0]-1:comp_xy[0]+1, comp_xy[1]-1:comp_xy[1]+1] = 1 ;; only use the center 9 pixel to locate the companion obj
  PSF0 = mrdfits('./PSFs/'+PSF_fn[minID], /silent)
  comp_xy = registerPSF(im_subbed, PSF0, err, mask3, [18, 10])

  ;;; fit two PSFs
  PSF1 = psfList[*,*,minID]
  PSF2 = shiftPSF(psf0, comp_xy[0] - 13, comp_xy[1] - 13, factor = 10)
  mask40 = fltarr(27, 27)
  mask40[11:26,0:15] = 1 ;;; only calculate the fourth quan
  mask4 = make_mask(mask, [[[xy[0], xy[1], 0, 3], [xy[0], xy[1], 12, 100]]])*mask40
  amps = fit2PSFs(im, err, PSF1, PSF2, mask4)
  p = plotFitResult(im, PSF1*amps[0], PSF2*amps[1], round(comp_xy))
  stop
END
