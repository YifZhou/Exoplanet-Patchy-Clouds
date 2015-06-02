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
  forward_FUNCTION fit1PSF
  dxy0 = [13, 13] - gc
  ngrid = 5 ;;; number of grid on each side
  grid = fltarr(ngrid, ngrid)  ;;; initalize the grid point
  gridSize = 0.4               ;;; inital lize the distance of lence of the grid on each side
                               ;;; the total lence is 2 * gridSize,
                               ;;; which means the grid covers a
                               ;;; square whose edge is gridSize away
                               ;;; from the center
  WHILE gridsize GT 1e-3 DO BEGIN
     gridx = gc[0] + (findgen(ngrid) - ngrid/2) * gridSize/float(ngrid/2) ;;; x coordinate of each grid point
     gridy = gc[1] + (findgen(ngrid) - ngrid/2) * gridSize/float(ngrid/2) ;;; y coordinate of each grid point
     FOR i=0,ngrid-1 DO BEGIN
        FOR j=0,ngrid-1 DO BEGIN
           psf = shiftPSF(psf0, (gridx[i]-13), (gridy[j]-13), factor = 10)
           optPara = fit1PSF(im, psf, mask, weight = 1/err^2)
           grid[i, j] = optPara[2]
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

FUNCTION fit1PSF, im, psf, mask, weight = weight
  ;;; use least chisq fit to calculate the amplitude of PSF, and
  ;;; return the amplitude and reduced residual
  ;;; mod = a*PSF + b
  IF N_elements(weight) EQ 0 THEN weight = im - im + 1 ;;; default value for the weight array is a ones array

  A = [[total(mask*(PSF^2 * weight)), total(mask*(PSF*weight))],$
       [total(mask*(PSF*weight)), total(mask*weight)]]
  b = [[total(mask*(im*PSF*weight))], [total(mask*(im*weight))]]
  amp = LA_invert(A) ## b   ;;; calculate the amplitude of the residual by least chisq fit
  res = total(mask * (weight*(im - psf*amp[0] - amp[1])^2))/total(mask)    ;;; calculate the residual, only use the pixels that are not masked
  return, [amp[0], amp[1], sqrt(res)]
END

FUNCTION fit2PSFs, im, PSF1, PSF2, mask, weight = weight
  ;;; fit two PSf to one image to calculate the flux of secondary
  ;;; PSF1: PSF of the primary
  ;;; PSF2: PSF of the secondary
  ;;; return the amplitude of two PSFs
  IF N_elements(weight) EQ 0 THEN weight = im - im + 1 ;;; default value for the weight array is a ones array
  A = [[total(mask*(PSF1^2*weight)), total(mask*(PSF1*PSF2*weight)), total(mask*(PSF1*weight))],$
       [total(mask*(PSF1*PSF2*weight)), total(mask*(PSF2^2*weight)), total(mask*(PSF2*weight))],$
       [total(mask*(PSF1*weight)), total(mask*(PSF2*weight)), total(mask*weight)]]
  b = [[total(mask*(PSF1*im*weight))], [total(mask*(PSF2*im*weight))], total(mask*(im*weight))]
  amp = LA_invert(A) ## b
  res = total(mask * (weight*(im - PSF1*amp[0] -PSF2*amp[1]- amp[2])^2))/total(mask)
  return, [amp[0], amp[1], amp[2], res]
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
  p=plot(PSF1[im_c[0]-5:im_c[0]+5,im_c[1] - 1],'b:', /stairstep, layout = [3,2,1], /current,/overplot,/ylog)
  p=plot(PSF2[im_c[0]-5:im_c[0]+5,im_c[1] - 1],'m--', /stairstep, layout = [3,2,1], /current,/overplot,/ylog)
  p=plot(PSF[im_c[0]-5:im_c[0]+5,im_c[1] - 1],'g2', /stairstep, layout = [3,2,1], /current,/overplot,/ylog)
  
  p=plot(im[im_c[0]-5:im_c[0]+5,im_c[1]],'r+', layout = [3,2,2], /current, /ylog)
  p=plot(PSF1[im_c[0]-5:im_c[0]+5,im_c[1]],'b:', /stairstep, layout = [3,2,2], /current,/overplot,/ylog)
  p=plot(PSF2[im_c[0]-5:im_c[0]+5,im_c[1]],'m--', /stairstep, layout = [3,2,2], /current,/overplot,/ylog)
  p=plot(PSF[im_c[0]-5:im_c[0]+5,im_c[1]],'g2', /stairstep, layout = [3,2,2], /current,/overplot,/ylog)

  p=plot(im[im_c[0]-5:im_c[0]+5,im_c[1]+1],'r+', layout = [3,2,3], /current, /ylog)
  p=plot(PSF1[im_c[0]-5:im_c[0]+5,im_c[1]+1],'b:', /stairstep, layout = [3,2,3], /current,/overplot,/ylog)
  p=plot(PSF2[im_c[0]-5:im_c[0]+5,im_c[1]+1],'m--', /stairstep, layout = [3,2,3], /current,/overplot,/ylog)
  p=plot(PSF[im_c[0]-5:im_c[0]+5,im_c[1]+1],'g2', /stairstep, layout = [3,2,3], /current,/overplot,/ylog)

  p=plot(im[im_c[0]-1, im_c[1]-5:im_c[1]+5],'r+', layout = [3,2,4], /current, /ylog)
  p=plot(PSF1[im_c[0]-1, im_c[1]-5:im_c[1]+5],'b:', /stairstep, layout = [3,2,4], /current,/overplot,/ylog)
  p=plot(PSF2[im_c[0]-1, im_c[1]-5:im_c[1]+5],'m--', /stairstep, layout = [3,2,4], /current,/overplot,/ylog)
  p=plot(PSF[im_c[0]-1, im_c[1]-5:im_c[1]+5],'g2', /stairstep, layout = [3,2,4], /current,/overplot,/ylog)

  p=plot(im[im_c[0], im_c[1]-5:im_c[1]+5],'r+', layout = [3,2,5], /current, /ylog)
  p=plot(PSF1[im_c[0], im_c[1]-5:im_c[1]+5],'b:', /stairstep, layout = [3,2,5], /current,/overplot,/ylog)
  p=plot(PSF2[im_c[0], im_c[1]-5:im_c[1]+5],'m--', /stairstep, layout = [3,2,5], /current,/overplot,/ylog)
  p=plot(PSF[im_c[0], im_c[1]-5:im_c[1]+5],'g2', /stairstep, layout = [3,2,5], /current,/overplot,/ylog)
 
  p=plot(im[im_c[0]+1, im_c[1]-5:im_c[1]+5],'r+', layout = [3,2,6], /current, /ylog)
  p=plot(PSF1[im_c[0]+1, im_c[1]-5:im_c[1]+5],'b:', /stairstep, layout = [3,2,6], /current,/overplot,/ylog)
  p=plot(PSF2[im_c[0]+1, im_c[1]-5:im_c[1]+5],'m--', /stairstep, layout = [3,2,6], /current,/overplot,/ylog)
  p=plot(PSF[im_c[0]+1, im_c[1]-5:im_c[1]+5],'g2', /stairstep, layout = [3,2,6], /current,/overplot,/ylog)
  return, p
END

function PSFPhotometry, fn, filterName, angle, dither, xy0
  ;;; use tinytim PSF to measure the photometry
  ;;; input parameter:
  ;;; fn: filename of the input flt file\
  ;;; angle: position angle of HST for the exposure
  ;;; dither: dither position for the exposure
  ;;; xy0: position for the peak pixel of the PSF
  forward_FUNCTION findpeak
  imagePath = '../data/2M1207B/'
  im = mrdfits(imagePath + fn, 1)
  im = im[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  err = mrdfits(imagePath + fn, 2)
  err = err[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  dq = mrdfits(imagePath + fn, 3)
  dq = dq[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  ;;; after this, the center of the image went to [13, 13]
  PSFPath = './PSF/angle_' + strn(angle) + '_dither_' + strn(angle) + '/'
  readcol, PSFPath + 'fn.dat', PSF_fn, format = 'a' ;; read in all fits file names
  amp = fltarr(2, N_elements(PSF_fn))
  res = fltarr(N_elements(PSF_fn))
  jitx = fltarr(N_elements(PSF_fn))
  jity = fltarr(N_elements(PSF_fn))
  dis = fltarr(N_elements(PSF_fn))
  PSFList = fltarr(27, 27, N_elements(PSF_fn))
  mask = maskoutdq(dq)
  fixpix, im, mask, im_fixed
  xy = findpeak(im_fixed, 13, 13, range=5)
  print, xy
  IF angle EQ 0 THEN comp_xy = [18,10] ELSE comp_xy = [16, 8]
  xyList = make_array(N_elements(PSF_fn), 2, /float)
  for i=0, N_elements(PSF_fn) - 1 DO BEGIN 
     psf0 = mrdfits(PSFPath+PSF_fn[i],/silent)
     psf0 = psf0[1:270, 1:270] ;; weird enough, 10x sampling PSF return ed by TinyTim has a size of 272*272, instead of 27*27. Thus, trim off the edge pixels
     mask1 = make_mask(mask,[[comp_xy[0], comp_xy[1], 0, 3], [13, 13, 11, 100]])
     xy = registerPSF(im, psf0, err, mask1, xy)
     xyList[i, *] = xy
     dxy = xy - [13, 13] ;; the displacement of the center of the image to the center of the psf
     psf = shiftPSF(psf0, dxy[0], dxy[1], factor = 10)
     mask2 = make_mask(mask, [[xy[0], xy[1], 0, 3], [comp_xy[0], comp_xy[1], 0, 3], [xy[0], xy[1], 12, 100]])
     opt_paras = fit1PSF(im, psf, mask2, weight = 1/err^2)
     amp[0, i] = opt_paras[0]
     amp[1, i] = opt_paras[1]
     res[i] = opt_paras[2]
     jitx[i] = float(strmid(PSF_fn[i], 5, 2))
     jity[i] = float(strmid(PSF_fn[i], 13, 2))
     dis[i] = float(strmid(PSF_fn[i], 20, 4))
     print,'PSF name: ', PSF_fn[i]
     print,'opimized rms residual: ', res[i]
     PSFList[*, *, i] = psf
  ENDFOR
  minID = (where(res EQ min(res)))[0]
  im_subbed = im - psfLIST[*,*,minID] * amp[0, minID] - amp[1, minID]
  xy = xyList[minID, *] ;; center of the primary
  PSF_box = im_subbed[comp_xy[0]-2:comp_xy[0]+2, comp_xy[1]-2:comp_xy[1]+2]
  maxBox = max(PSF_box, maxID)
  PSF_x_cood = maxID MOD 5
  PSF_y_cood = maxID/5
  comp_xy = comp_xy - [2, 2] + [PSF_x_cood, PSF_y_cood] ;; use the peak pixel in a 5x5 box as the initial guess for the center of the companion obj.
  comp_xy0 = comp_xy - [13,13] + xy0       ;;; the peak pixel of the companion obj in original image
  spawn, 'python PSF_generator.py ' + strn(comp_xy0[0]) + ' ' + strn(comp_xy0[1])$
         + ' ' + filterName + ' ' + strn(jitx[minID]) + ' ' + strn(jity[minID])$
         + ' ' + strn(dis[minID]) + ' comp_PSF' ;; use tinytim to generate a PSF file that works for  companion

  PSF0 = mrdfits('comp_PSF00.fits')
  mask3 = mask
  mask3 = fltarr(27, 27)
  mask3[comp_xy[0]-1:comp_xy[0]+1, comp_xy[1]-1:comp_xy[1]+1] = 1 ;; only use the center 9 pixel to locate the companion obj
  comp_xy = registerPSF(im_subbed, PSF0, err, mask3, comp_xy)

  ;;; fit two PSFs
  PSF1 = psfList[*,*,minID]
  PSF2 = shiftPSF(psf0, comp_xy[0] - 13, comp_xy[1] - 13, factor = 10)
  mask40 = fltarr(27, 27)
  mask40[11:26,0:15] = 1 ;;; only calculate the fourth quadrant
  mask4 = make_mask(mask, [[[xy[0], xy[1], 0, 3], [xy[0], xy[1], 12, 100]]])*mask40
  amps = fit2PSFs(im, PSF1, PSF2, mask4, weight = 1/err^2)
  writefits, './fitsResult/'+strmid(fn, 0, 9) + '.fits', im
  writefits, './fitsResult/'+strmid(fn, 0, 9) + '.fits', PSF1*amps[0] + PSF2*amps[1]+amps[2], /append
  ;; Set_Plot, 'Z', /COPY
  ;; p = plotFitResult(im, PSF1*amps[0], PSF2*amps[1], round(comp_xy))
  ;; p.Save, './fitPlots/' + strmid(fn, 0, 9) + '.pdf', resolution = 300, /transparent
  ;; p.Close
  
  return, amps
END

function PSFPhotometry1, fn, filterName, angle, dither, xy0
  ;;; use tinytim PSF to measure the photometry
  ;;; input parameter:
  ;;; fn: filename of the input flt file\
  ;;; angle: position angle of HST for the exposure
  ;;; dither: dither position for the exposure
  ;;; xy0: position for the peak pixel of the PSF
  forward_FUNCTION findpeak
  imagePath = '../data/2M1207B/'
  imhd= mrdfits(imagePath +fn, 0, hd)
  MJD = fxpar(hd, 'EXPSTART')
  im = mrdfits(imagePath + fn, 1)
  im = im[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  err = mrdfits(imagePath + fn, 2)
  err = err[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  dq = mrdfits(imagePath + fn, 3)
  dq = dq[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  ;;; after this, the center of the image went to [13, 13]
  mask = maskoutdq(dq)
  fixpix, im, mask, im_fixed
  xy1 = findpeak(im_fixed, 13, 13, range=5)
  print, xy1
  IF angle EQ 0 THEN comp_xy = [18,10] ELSE comp_xy = [16, 8]
  spawn, 'python PSF_generator.py ' + strn(xy0[0]) + ' ' + strn(xy0[1])$
         + ' ' + filterName + ' ' + strn(-1) + ' ' + strn(-1)$
         + ' ' + strn(MJD) + ' ./PSF/temp' ;; use tinytim to generate a PSF file that works for  companion
  psf0 = mrdfits('./PSF/temp00.fits',/silent)
  psf0 = psf0[1:270, 1:270] ;; weird enough, 10x sampling PSF return ed by TinyTim has a size of 272*272, instead of 27*27. Thus, trim off the edge pixels
  mask1 = make_mask(mask,[[comp_xy[0], comp_xy[1], 0, 3], [13, 13, 11, 100]])
  xy = registerPSF(im, psf0, err, mask1, xy1)
  dxy = xy - [13, 13] ;; the displacement of the center of the image to the center of the psf
  psf = shiftPSF(psf0, dxy[0], dxy[1], factor = 10)
  mask2 = make_mask(mask, [[xy[0], xy[1], 0, 3], [comp_xy[0], comp_xy[1], 0, 3], [xy[0], xy[1], 12, 100]])
  opt_paras = fit1PSF(im, psf, mask2, weight = 1/err^2)

  im_subbed = im - psf * opt_paras[0] - opt_paras[1]
  PSF_box = im_subbed[comp_xy[0]-2:comp_xy[0]+2, comp_xy[1]-2:comp_xy[1]+2]
  maxBox = max(PSF_box, maxID)
  PSF_x_cood = maxID MOD 5
  PSF_y_cood = maxID/5
  comp_xy = comp_xy - [2, 2] + [PSF_x_cood, PSF_y_cood] ;; use the peak pixel in a 5x5 box as the initial guess for the center of the companion obj.
  comp_xy0 = comp_xy - [13,13] + xy0                    ;;; the peak pixel of the companion obj in original image
  
  spawn, 'python PSF_generator.py ' + strn(comp_xy0[0]) + ' ' + strn(comp_xy0[1])$
         + ' ' + filterName + ' ' + strn(-1) + ' ' + strn(-1)$
         + ' ' + strn(MJD) + ' comp_PSF' ;; use tinytim to generate a PSF file that works for  companion

  PSF0 = mrdfits('comp_PSF00.fits')
  mask3 = mask
  mask3 = fltarr(27, 27)
  mask3[comp_xy[0]-1:comp_xy[0]+1, comp_xy[1]-1:comp_xy[1]+1] = 1 ;; only use the center 9 pixel to locate the companion obj
  comp_xy = registerPSF(im_subbed, PSF0, err, mask3, comp_xy)

  ;;; fit two PSFs
  PSF1 = psf
  PSF2 = shiftPSF(psf0, comp_xy[0] - 13, comp_xy[1] - 13, factor = 10)
  mask40 = fltarr(27, 27)
  mask40[11:26,0:15] = 1 ;;; only calculate the fourth quadrant
  mask4 = make_mask(mask, [[[xy[0], xy[1], 0, 3], [xy[0], xy[1], 12, 100]]])*mask40
  amps = fit2PSFs(im, PSF1, PSF2, mask4, weight = 1/err^2)
  print,'opimized rms residual: ', amps[3]
  writefits, './fitsResult/'+strmid(fn, 0, 9) + '.fits', im
  writefits, './fitsResult/'+strmid(fn, 0, 9) + '.fits', PSF1*amps[0] + PSF2*amps[1]+amps[2], /append
  ;; Set_Plot, 'Z', /COPY
  ;; p = plotFitResult(im, PSF1*amps[0], PSF2*amps[1], round(comp_xy))
  ;; p.Save, './fitPlots/' + strmid(fn, 0, 9) + '.pdf', resolution = 300, /transparent
  ;; p.Close
  
  return, amps
END

PRO tinytimPSF, infoFile
  forward_FUNCTION myReadCSV
  fileInfo = myReadCSV(infoFile, ['filename', 'filter', 'orbit', 'PosAngle', 'dither', 'exposureset', 'obsdate', 'obstime', 'expoTime'])
  xy = [[[135,161], [145,161], [135,173], [145,173]],$
      [[142, 159],[152,159], [142, 171], [152, 171]]]
  fileInfo.PosAngle = (fileInfo.orbit + 1) MOD 2
  F125ID = where(fileInfo.filter EQ 'F125W')
  fluxA = fltarr(N_elements(F125ID))
  fluxB = fltarr(N_elements(F125ID))
  sky = fltarr(N_elements(F125ID))
  chisq = fltarr(N_elements(F125ID))
  FOR i=0, N_elements(F125ID) - 1 DO BEGIN
     id = F125ID[i]
     a = PSFPhotometry1(fileInfo.filename[id], fileInfo.filter[id], long(fileInfo.PosAngle[id]), long(fileInfo.dither[id]), xy[*, long(fileInfo.dither[id]), long(fileInfo.posAngle[id])])
     fluxA[i] = a[0]
     fluxB[i] = a[1]
     sky[i] = a[2]
     chisq[i] = a[3]
  ENDFOR
  forprint, fileInfo.filename[F125ID], fileInfo.orbit[F125ID], fileInfo.obsdate[F125ID], fileInfo.obstime[F125ID], fileInfo.expoTime[F125ID], fluxA, fluxB, sky, chisq, textout = 'F125Flux.dat', width = 320, /NoCOMMENT
  stop
END
