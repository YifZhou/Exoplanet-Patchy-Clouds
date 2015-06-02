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
  
  ;;psf = resample(fshift(psf0, dx*factor, dy*factor), size0/factor,
  ;;size0/factor)
  psf = resample(my_shift2d(psf0, [dx*factor, dy*factor], cubic = 1), size0/factor, size0/factor)
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

function PSFPhotometry, im, err, dq, filterName, angle, dither, xy0
  ;;; use tinytim PSF to measure the photometry
  ;;; adapted from psf photometry routine from 2M1207's pipeline
  ;;; fn: filename of the input flt files
  ;;; angle: position angle of HST for the exposure
  ;;; dither: dither position for the exposure
  ;;; xy0: position for the peak pixel of the PSF
  PSFPath = './PSF/filter_'+filterName+'_angle_' + strn(angle) + '_dither_' + strn(angle) + '/'
  readcol, PSFPath + 'fn.dat', PSF_fn, format = 'a' ;; read in all fits file names
  im = im[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  err = err[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  dq = dq[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  amp = fltarr(N_elements(PSF_fn))
  sky = fltarr(N_elements(PSF_fn))
  res = fltarr(N_elements(PSF_fn))
  jitx = fltarr(N_elements(PSF_fn))
  jity = fltarr(N_elements(PSF_fn))
  dis = fltarr(N_elements(PSF_fn))
  PSFList = fltarr(27, 27, N_elements(PSF_fn))
  mask = maskoutdq(dq)
  fixpix, im, mask, im_fixed
  xy1 = findpeak(im_fixed, 13, 13, range=5)
  xyList = make_array(N_elements(PSF_fn), 2, /float)
  for i=0, N_elements(PSF_fn) - 1 DO BEGIN 
     psf0 = mrdfits(PSFPath+PSF_fn[i],/silent)
     psf0 = psf0[1:270, 1:270] ;; weird enough, 10x sampling PSF return ed by TinyTim has a size of 272*272, instead of 27*27. Thus, trim off the edge pixels
     mask1 = make_mask(mask, [[13, 13, 8, 100]])
     xy = registerPSF(im, psf0, err, mask1, xy1)
     xyList[i, *] = xy
     dxy = xy - [13, 13] ;; the displacement of the center of the image to the center of the psf
     psf = shiftPSF(psf0, dxy[0], dxy[1], factor = 10)
     mask2 = make_mask(mask, [[xy[0], xy[1], 8, 100]])
     opt_paras = fit1PSF(im, psf, mask2, weight = 1/err^2)
     amp[i] = opt_paras[0]
     sky[i] = opt_paras[1]
     res[i] = opt_paras[2]
     jitx[i] = float(strmid(PSF_fn[i], 5, 2))
     jity[i] = float(strmid(PSF_fn[i], 13, 2))
     dis[i] = float(strmid(PSF_fn[i], 20, 4))
     ;; print,'PSF name: ', PSF_fn[i]
     ;; print,'opimized rms residual: ', res[i]
     PSFList[*, *, i] = psf
  ENDFOR
  minID = (where(res EQ min(res)))[0]
  print, 'Best fitted PSF, Jitx = ', jitx[minID], ', Jity = ', jity[minID], 'Dis = ', dis[minID]
  amps = [amp[minID], sky[minID], xyList[minID, 0]-13+xy0[0], xyList[minID, 1]-13+xy0[1]]
  return, amps
END

FUNCTION PSFPhotometry1, im, err, dq, MJD, filterName, angle, dither, xy0
  ;;; use the focus model, only try one PSFf
  im = im[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  err = err[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  dq = dq[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  mask = maskoutdq(dq)
  mask1 = make_mask(mask, [[13, 13, 5, 100]])
  fixpix, im, mask, im_fixed
  xy1 = findpeak(im_fixed, 13, 13, range=5)
  ;; jitx = [0, 10, 20, 30]
  ;; jity = [0, 10, 20, 30]
  ;; resGrid = fltarr(4, 4)
  ;; FOR i = 0, 3 DO BEGIN
  ;;    FOR j = 0, 3 DO BEGIN
  ;;       spawn, 'python PSF_generator.py ' + strn(xy0[0]) + ' ' + strn(xy0[1])$
  ;;              + ' ' + filterName + ' ' + strn(jitx[i]) + ' ' + strn(jity[j])$
  ;;              + ' ' + strn(MJD) + ' ./PSF/temp' ;; use tinytim to generate a PSF file that works for  companion
  ;;       psf0 = mrdfits('./PSF/temp00.fits',/silent)
  ;;       psf0 = psf0[1:270, 1:270] ;; weird enough, 10x sampling PSF return ed by TinyTim has a size of 272*272, instead of 27*27. Thus, trim off the edge pixels
  ;;       xy = registerPSF(im, psf0, err, mask1, xy1)
  ;;       dxy = xy - [13, 13] ;; the displacement of the center of the image to the center of the psf
  ;;       psf = shiftPSF(psf0, dxy[0], dxy[1], factor = 10)
  ;;       mask2 = make_mask(mask, [[xy[0], xy[1], 5, 100]])
  ;;       opt_paras = fit1PSF(im, psf, mask2, weight = 1/err^2)
  ;;       resGrid[i, j] = opt_paras[2]
  ;;    ENDFOR     
  ;; ENDFOR
  spawn, 'python PSF_generator.py ' + strn(xy0[0]) + ' ' + strn(xy0[1])$
               + ' ' + filterName + ' ' + strn(-1) + ' ' + strn(-1)$
               + ' ' + strn(MJD) + ' ./PSF/temp' ;; use tinytim to generate a PSF file that works for  companion
  psf0 = mrdfits('./PSF/temp00.fits',/silent)
  psf0 = psf0[1:270, 1:270] ;; weird enough, 10x sampling PSF return ed by TinyTim has a size of 272*272, instead of 27*27. Thus, trim off the edge pixels
  xy = registerPSF(im, psf0, err, mask1, xy1)
  dxy = xy - [13, 13] ;; the displacement of the center of the image to the center of the psf
  psf = shiftPSF(psf0, dxy[0], dxy[1], factor = 10)
  mask2 = make_mask(mask, [[xy[0], xy[1], 5, 100]])
  opt_paras = fit1PSF(im, psf, mask2, weight = 1/err^2)
  IF opt_paras[2] GT 6 THEN stop 
  amps = [opt_paras[0:1], xy - 13 + xy0]
  print, 'fitting reduced Chisq = ', opt_paras[2]
  return, amps
END


PRO tinytimPSF
  ;;; use primary subtracted file from aperture photometry to test
  ;;; whehter tinyTim PSF fit measurement is better than aperture
  ;;; photometry
  subtractedFile = '2015_May_07_subtracted.sav'
  restore, subtractedFile
  dataDIR = '../data/ABPIC-B_noramp/'
  infoFile = '2015_May_07_noramp_aper=5.00_result.csv'
  fileInfo = myReadCSV(infoFile, ['FILENAME','FILTER','ORBIT','POSANG','DITHER','EXPOSURE_SET','OBS_DATE','OBS_TIME','EXPOSURE_TIME','XOFF','YOFF','XCENTER','YCENTER','PSF_ID','PSF_AMPLITUTE','SKY_LEVEL','SKY_SIGMA','FLUX','FLUXERR','XFWHM','YFWHM','CONTAMINATED'])
  

  xy = [[[95,208], [105,208], [95,219], [105,219]],$
      [[129, 222],[139,222], [129, 233], [139, 233]]]
  fileInfo.PosAng = (fileInfo.orbit + 1) MOD 2
  flux = fltarr(N_elements(fileInfo.filename))
  sky = fltarr(N_elements(fileInfo.filename))
  xfit = fltarr(N_elements(fileInfo.filename))
  yfit = fltarr(N_elements(fileInfo.filename))
  FOR i=0, N_elements(fileInfo.fileName) - 1 DO BEGIN
     print, 'FILE: ', fileInfo.filename[i]
     hdrim = mrdfits(dataDIR + fileInfo.filename[i], 0, hd,/silent)
     MJD = fxpar(hd, 'EXPSTART')
     dq = mrdfits(dataDIR + fileInfo.filename[i], 3,/silent)
     im = cube1[*,*,i]
     err = errorcube[*,*,i]
     ;;a = PSFPhotometry(im, err, dq, fileInfo.Filter[i], long(fileInfo.Posang[i]), long(fileInfo.dither[i]), xy[*, long(fileinfo.dither[i]), long(fileInfo.posang[i])])
     a = PSFPhotometry1(im, err, dq, MJD, fileInfo.Filter[i], long(fileInfo.Posang[i]), long(fileInfo.dither[i]), xy[*, long(fileinfo.dither[i]), long(fileInfo.posang[i])])
     flux[i] = a[0]
     sky[i] = a[1]
     xfit[i] = a[2]
     yfit[i] = a[3]
  ENDFOR
  infoStruct1 = add_tag(infoStruct1, 'flux_fit', flux)
  infoStruct1 = add_tag(infoStruct1, 'x_fit', xfit)
  infoStruct1 = add_tag(infoStruct1, 'y_fit', yfit)
  infoStruct1 = add_tag(infoStruct1, 'skyy_fit', sky)
  save, infoStruct1, file = 'ABPIC-B_tinyTim_fit.sav'
  spawn, 'python sav2csv.py ABPIC-B_tinyTim_fit.sav ABPIC-B_tinyTim_fit.csv' ;; convert .sav file to csv file for easier using.
  stop
END
