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
  return, [amp[0], amp[1], res]
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

FUNCTION shiftPSF, psf0, dx, dy, factor = factor
  ;; shift the over-sampled PSF using fshift, which implement bilinear
  ;; interpolation to shift the PSFs. After shift the PSF, resample
  ;; the PSF using the sample rate OF the origial image. Finally,
  ;; convolove the image with a intrapixel diffusion core.
  ;; not every pixel in PSF0 is useful actually
  ;; if specify a PSF size of 3 arcsec by 3 arcsec, it generates a
  ;; 2.957 by 2.957 arcsec PSFs in order to keep the size of the
  ;; production of tiny2 integer ( 2.957 = 82 * 0.03606)
  ;; 
  ;; the production of tiny3 with 10x super sampling ends up with a
  ;; size of 272*272. However, for WFC3 IR, x and y direction has
  ;; different pixel scale,
  ;; for x direction, it is 0.135 arcsec/pixel
  ;; while for y direction, it is 0.121 arcsec/pixel.
  ;; number 272 comes from using an approximate pixel size of 0.13
  ;; arcsec/pixel
  ;; and 272 = int(2.957/0.13 * 10 * 1.2) (1.2 is a padding factor)
  ;; The non-zero pixels in the super sampled PSFs ranges from
  ;; x = 27 : 244 (218 pixels, 2.957/0.135*10 = 219)
  ;; y = 14: 256 (243 pixels, 2.957/0.121*10 = 244.3) ;; both x and y
  ;; starts with 0
  ;; instead of bin a 270x270 PSF to 27x27, we should bin a 219x244 to
  ;; 21.9x24.4 to keep a correct geometric distortion correction
  ;; dan zhe bing mei shenme luan yong
  
  ;; input parameter:
  ;; dx, dy: the shift distance in x AND y direction. The pixel sizes FOR both dx AND dy are the same as the original image, instead OF oversampled PSF
  ;; factor: the oversample rate, default value is 10
  
  ;;IF N_elements(factor) EQ 0 THEN factor = 10
  ;; default super sample factor is 9
  PSF_core = [[0.0007, 0.025005,  0.0007],$
              [0.025005,  0.89718,  0.025005],$
              [0.0007, 0.025005, 0.0007]] ;; intrapixel diffusion core. convol this with the resampled PSF, as indicated by tiny tim manual.
  IF N_elements(factor) EQ 0 THEN factor = 9
  size0 = (size(psf0))[1]
  peak_xy = size0/2 ;; the x and y coordinate of the peak of the oversampled

  ;;Step One, shift
  ;;psf = fshift(psf0, dx*factor, dy*factor) ;; dont use fshift,
  ;;instead, using bicubic interpolation to do the shift, which is
  ;;done by my_shift2d
  psf = my_shift2d(psf0, dx*factor, dy*factor, cubic = 1)

  ;;Step Two, select sub region
  ;; the effective PSF will be 27x27 pixels, or 3x3 arcsec
  ;; convolve a N x N array with a 3x3 array, the effective region of
  ;; the result will be a (N-2) x (N-2) array ( N-2 = N-3+1)
  ;; so generate a 29x29 array first
  ;; so the suzbsize will be 29*9 = 261 and 261/2 = 130
  psf = psf[peak_xy - 130: peak_xy + 130, peak_xy - 130: peak_xy + 130]

  ;;Step Three, rebin the psf, using frebin
  psf = frebin(psf, 29, 29, /total)
  
  ;;Step Four, convolve with a PSF core
  psf = convol(psf, PSF_core) ;; a 29*29 array
  return, psf[1:27, 1:27] ;; finally, return a 27*27 array
END


FUNCTION fit2PSFs_res, im, PSF1, PSF2, residual, mask, weight = weight
  ;;; fit two PSf to one image to calculate the flux of secondary
  ;;; PSF1: PSF of the primary
  ;;; PSF2: PSF of the secondary
  ;;; return the amplitude of two PSFs
  IF N_elements(weight) EQ 0 THEN weight = im - im + 1 ;;; default value for the weight array is a ones array
  A = [[total(mask*(PSF1^2*weight)), total(mask*(PSF1*PSF2*weight)), total(mask*(PSF1*residual*weight)), total(mask*(PSF1*weight))],$
       [total(mask*(PSF1*PSF2*weight)), total(mask*(PSF2^2*weight)), total(mask*(PSF2*residual*weight)),total(mask*(PSF2*weight))],$
       [total(mask*(PSF1*residual*weight)), total(mask*(PSF2*residual*weight)), total(mask*(residual^2*weight)),total(mask*(residual*weight))],$
       [total(mask*(PSF1*weight)), total(mask*(PSF2*weight)), total(mask*(residual*weight)),total(mask*weight)]]
  b = [[total(mask*(PSF1*im*weight))], [total(mask*(PSF2*im*weight))], [total(mask*(residual*im*weight))], [total(mask*(im*weight))]]
  invA = LA_invert(A)
  amp = invA ## b
  err = sqrt(diag_matrix(invA))
  res = total(mask * (weight*(im - PSF1*amp[0] -PSF2*amp[1]- residual * amp[2] - amp[3])^2))/total(mask)
  return, [amp[0], amp[1], amp[3], res, amp[2], err[0], err[1]] ;; put the amplitude for residual at th end
END

FUNCTION registerPSF, im, psf0, mask, gc, weight = weight
  ;; register psf AND image by minizing the residual
  ;; return the center of the image
  ;; center of resampled psf is always at [13, 13]
  
  ;; in put paramenters:
  ;; im: the original image, center is around [13, 13]
  ;; PSF0: tinytim PSF, 10x oversampled, 270x270 in size, after resampling to wfc3 ir sample rate, center is [13, 13]
  ;; err: error array extracted from fits file, used FOR calculate chisq
  ;; mask: a 0-1 array to indicate which pixel to be masked out. 1 stands FOR transparent AND 0 stands FOR mask
  ;; gc: initial value FOR grid center
  IF N_elements(weight) EQ 0 THEN weight = im - im + 1 ;;; default value for the weight array is a ones array
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
           psf = shiftPSF(psf0, (gridx[i]-13), (gridy[j]-13), factor = 9)
           optPara = fit1PSF(im, psf, mask, weight = weight)
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

FUNCTION register2PSFs, im, PSF1, PSF02, mask, gc, weight = weight
  ;;; PSF1 is fixed, using detector sample rate, PSF2 uses 10x sample rate
  dxy0 = [13, 13] - gc
  ngrid = 5 ;;; number of grid on each side
  grid = fltarr(ngrid, ngrid)  ;;; initalize the grid point
  gridSize = 1.0               ;;; inital lize the distance of lence of the grid on each side
                               ;;; the total lence is 2 * gridSize,
                               ;;; which means the grid covers a
                               ;;; square whose edge is gridSize away
                               ;;; from the center
  WHILE gridsize GT 1e-2 DO BEGIN
     gridx = gc[0] + (findgen(ngrid) - ngrid/2) * gridSize/float(ngrid/2) ;;; x coordinate of each grid point
     gridy = gc[1] + (findgen(ngrid) - ngrid/2) * gridSize/float(ngrid/2) ;;; y coordinate of each grid point
     FOR i=0,ngrid-1 DO BEGIN
        FOR j=0,ngrid-1 DO BEGIN
           PSF2 = shiftPSF(PSF02, (gridx[i]-13), (gridy[j]-13), factor = 9)
           optPara = fit2PSFs(im, PSF1, PSF2, mask, weight = weight)
           grid[i, j] = optPara[3]
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

function PSFPhotometry, im, err, dq, PSF01, PSF02, residual0
  ;;; use tinytim PSF to measure the photometry
  ;;; input parameter:
  ;;; fn: filename of the input flt file\
  ;;; angle: position angle of HST for the exposure
  ;;; dither: dither position for the exposure
  ;;; xy0: position for the peak pixel of the PSF

  ;;; after this, the center of the image went to [13, 13]
  mask = maskoutdq(dq)
  comp_xy = [18, 10]
  xy0 = [145, 173]
  fixpix, im, mask, im_fixed, /silent
  xy1 = findpeak(im_fixed, 13, 13, range=5)
  mask1 = make_mask(mask,[[comp_xy[0], comp_xy[1], 0, 3], [13, 13, 11, 100]])
  xy = registerPSF(im, PSF01, mask1, xy1, weight = 1/err^2)
  dxy = xy - [13, 13] ;; the displacement of the center of the image to the center of the psf
  PSF1= shiftPSF(PSF01, dxy[0], dxy[1], factor = 9)
  mask2 = make_mask(mask, [[xy[0], xy[1], 0, 3.0], [comp_xy[0], comp_xy[1], 0, 5]])
  opt_paras = fit1PSF(im, PSF1, mask2, weight = 1/err^2)
  amp = opt_paras[0]
  sky = opt_paras[1]
  im_subbed = im - PSF1 * amp - sky

  PSF_box = im_subbed[comp_xy[0]-2:comp_xy[0]+2, comp_xy[1]-2:comp_xy[1]+2]
  maxBox = max(PSF_box, maxID)
  PSF_x_cood = maxID MOD 5
  PSF_y_cood = maxID/5
  comp_xy = comp_xy - [2, 2] + [PSF_x_cood, PSF_y_cood] ;; use the peak pixel in a 5x5 box as the initial guess for the center of the companion obj.
  comp_xy0 = comp_xy - [13,13] + xy0                    ;;; the peak pixel of the companion obj in original image

  mask3 = mask
  mask3 = fltarr(27, 27)
  mask3[comp_xy[0]-1:comp_xy[0]+1, comp_xy[1]-1:comp_xy[1]+1] = 1           ;; only use the center 9 pixel to locate the companion obj
  comp_xy = registerPSF(im_subbed, PSF02, mask3, comp_xy, weight = 1/err^2) ;; caluate the center of secondary coarsely

  ;;; fit two PSFs
  mask40 = fltarr(27, 27)
  ;;mask40[11:26,0:15] = 1 ;;; only calculate the fourth quadrant
  mask4 = make_mask(mask, [[xy[0], xy[1], 0, 3.5]]) ;;*mask40
  
  ;;mask4 = make_mask(mask, [[xy[0], xy[1], 11, 100]])*mask40
  comp_xy = register2PSFs(im, PSF1, PSF02, mask4, comp_xy, weight = 1/err^2)
  PSF2 = shiftPSF(PSF02, comp_xy[0] - 13, comp_xy[1] - 13, factor = 9)
  ;;amps = fit2PSFs(im, PSF1, PSF2, mask4, weight = 1/err^2)
  amps = fit2PSFs_res(im + residual0, PSF1, PSF2, residual0, mask4, weight=1/err^2)

  
  return, [amps[0]/total(PSF1), amps[1]/total(PSF2), xy + xy0 - [13, 13], comp_xy + xy0 - [13, 13]]
END


PRO tinyTimMCFit, nLoop
  imagePath = '../data/2M1207B/'
  ;;fn = 'icdg01a1q_flt.fits' ;; F125W
  fn = 'icdg01a2q_flt.fits' ;; F160W
  filter = 'F160W'
  primaryTTFN = '2massA_'+filter+'.in' ;; primary Tinytim parameter input file
  companionTTFN = '2massB_'+filter+'.in' ;; companion Tinytim parameter input file
  
  xy0 = [145, 173]
  comp_xy0 = [150, 169]
  comp_xy = comp_xy0 - xy0 + [13, 13]
  restore, filter+'_residual.sav'
  im = mrdfits(imagePath + fn, 1, /silent)
  im = im[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  im = im - residual[*, *, 3]
  imhd= mrdfits(imagePath +fn, 0, hd, /silent)
  MJD = fxpar(hd, 'EXPSTART')
  err = mrdfits(imagePath + fn, 2,/silent)
  err = err[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  dq = mrdfits(imagePath + fn, 3,/silent)
  dq = dq[xy0[0]-13:xy0[0]+13, xy0[1]-13:xy0[1]+13]
  
  spawn, 'python PSF_generate_list.py ' + strn(xy0[0]) + ' ' + strn(xy0[1])$
         + ' ' + primaryTTFN + ' ' + ' ' + strn(MJD) + ' 1'  ;; use tinytim to generate a PSF file that works for  companion
  readcol, 'fn.dat', PSF_fn, format = 'a', /silent            ;; read in all fits file names
  nPSFs = N_elements(PSF_fn)
  ampList = fltarr(nPSfs)
  skyList = fltarr(nPSFs)
  resList = fltarr(nPSFs)
  PSFList = fltarr(27, 27, nPSFs)
  xyList = fltarr(2, nPSFs)
  jitxList = [0,0,0,0,0,10,10,10,10,10,20,20,20,20,20,30,30,30,30,30,40,40,40,40,40]
  jityList = [0,10,20,30,40,0,10,20,30,40,0,10,20,30,40,0,10,20,30,40,0,10,20,30,40]
  mask = maskoutdq(dq)
  xy1 = findpeak(im, 13, 13, range=5)
  FOR i = 0, nPSFs - 1 DO begin
     psf0 = mrdfits(PSF_fn[i],/silent)
     mask1 = make_mask(mask,[[comp_xy[0], comp_xy[1], 0, 5]])
     xy = registerPSF(im, psf0, mask1, xy1, weight = 1/err^2)
     dxy = xy - [13, 13] ;; the displacement of the center of the image to the center of the psf
     xyList[*, i] = xy
     PSF= shiftPSF(psf0, dxy[0], dxy[1], factor = 9)
     mask2 = make_mask(mask, [[xy[0], xy[1], 0, 3.0], [comp_xy[0], comp_xy[1], 0, 5]])
     opt_paras = fit1PSF(im, PSF, mask2, weight = 1/err^2)
     PSFList[*, *, i] = PSF
     ampList[i] = opt_paras[0]
     skyList[i] = opt_paras[1]
     resList[i] = opt_paras[2]
  ENDFOR
  minID = (where(resList EQ min(resList)))[0]
  PSF1 = PSFList[*, *, minID]
  jitx = jitxList[minID]
  jity = jityList[minID]
  xy = xyList[*, minID]
  print, jitx, jity
  spawn, 'python PSF_generator.py ' + strn(xy0[0]) + ' ' + strn(xy0[1])$
         + ' ' + primaryTTFN + ' ' + strn(jitx) + ' ' + strn(jity)$
         + ' ' + strn(MJD) + ' primary_PSF 1' ;; use tinytim to generate a PSF file that works for  companion
  PSF1 = mrdfits('primary_PSF00.fits', /silent)
  spawn, 'python PSF_generator.py ' + strn(comp_xy0[0]) + ' ' + strn(comp_xy0[1])$
         + ' ' + companionTTFN + ' ' + strn(jitx) + ' ' + strn(jity)$
         + ' ' + strn(MJD) + ' comp_PSF 1' ;; use tinytim to generate a PSF file that works for  companion
  PSF2 = mrdfits('comp_PSF00.fits', /silent)
  primary_X = fltarr(nLoop)
  primary_Y = fltarr(nLoop)
  primary_f = fltarr(nLoop)
  secondary_X = fltarr(nLoop)
  secondary_Y = fltarr(nLoop)
  secondary_f = fltarr(nLoop)  
  FOR i=0, nLoop - 1 DO BEGIN
     im1 = im + err * randomn(seed, 27, 27)
     a = PSFPhotometry(im1, err, dq, PSF1, PSF2, residual[*, *, 3])     
     primary_f[i] = a[0]
     secondary_f[i] = a[1]
     primary_x[i] = a[2]
     primary_y[i] = a[3]
     secondary_x[i] = a[4]
     secondary_y[i] = a[5]
     print, i
  ENDFOR
  forprint, primary_f, secondary_f, primary_x, primary_y, secondary_x, secondary_y, textout='TinyTimMCFit_'+filter+'result.dat', /nocomment
END

