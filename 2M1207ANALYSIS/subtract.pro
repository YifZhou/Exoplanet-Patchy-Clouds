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

FUNCTION registerPSF, im, psf0, err, mask
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
  imsize = (size(im))[1]
  xy1 = findpeak(im, imsize/2., imsize/2., range = imsize/20)
  xy2 = findpeak(psf0, imsize/2., imsize/2., range = imsize/20)
  dxy0 = xy2 - xy1 ;; the difference of the center of PSF and
  ngrid = 5 ;;; number of grid on each side
  grid = fltarr(ngrid, ngrid)  ;;; initalize the grid point
  gridSize = 5.0               ;;; inital lize the distance of lence of the grid on each side
                               ;;; the total lence is 2 * gridSize,
                               ;;; which means the grid covers a
                               ;;; square whose edge is gridSize away
                               ;;; from the center
  WHILE gridsize GT 1e-2 DO BEGIN
     gridx = xy1[0] + (findgen(ngrid) - ngrid/2) * gridSize/float(ngrid/2) ;;; x coordinate of each grid point
     gridy = xy1[1] + (findgen(ngrid) - ngrid/2) * gridSize/float(ngrid/2) ;;; y coordinate of each grid point
     FOR i=0,ngrid-1 DO BEGIN
        FOR j=0,ngrid-1 DO BEGIN
           psf = fshift(psf0, (gridx[i]-xy2), (gridy[j]-xy2))
           optPara = fit1PSF(im, psf, mask, weight = 1/err^2)
           grid[i, j] = optPara[2]
        ENDFOR
     ENDFOR
     gridid = (where(grid EQ min(grid)))[0]
     gridc = [0.0, 0.0]
     gridc[1] = gridid/ngrid
     gridc[0] = gridid MOD ngrid 
     newxy1 = [gridx[gridc[0]], gridy[gridc[1]]] ;;; find the x and y coordinate of the grid point that has the least residual
     diff = newxy1 - xy1
     xy1 = newxy1   ;;; renew the grid center
     gridSize = max([max(abs(diff)) * 2, gridSize/2])   ;;; renew the gridSize
  ENDWHILE
  
  return, xy2 - newxy1 ;;; return the offset of PSF and target image
END

PRO subtract, im, center1, center2, subim1, subim2, maskVar, nSamp = nSamp
  IF N_ELEMENTS(nSamp) EQ 0 THEN nSamp = 10
  c1 = findpeak(im, center1[0], center1[1], range = 5)
  c2 = findpeak(im, center2[0], center2[1], range = 5)
  c1 = floor(c1)
  c2 = floor(c2)
  subIm1 = im[c1[0]-20:c1[0]+19, c1[1]-20:c1[1]+19]
  subIm2 = im[c2[0]-20:c2[0]+19, c2[1]-20:c2[1]+19]
  mask = make_mask(fltarr(256, 256) + 1, maskVar)
  subMask = mask[c1[0]-20:c1[0]+19, c1[1]-20:c1[1]+19]
  ;; interpolation
  subim1_int = congrid(subIm1, 40*nSamp, 40*nSamp, cubic = -0.5, /MINUS_ONE)
  subim2_int = congrid(subIm2, 40*nSamp, 40*nSamp, cubic = -0.5, /MINUS_ONE)
  subMask = congrid(subMask, 40*nSamp, 40*nSamp, /minus_one)
  c1 = findpeak(subim1, 40*nSamp/2, 40*nSamp/2, range = 3*nSamp)
  c2 = findpeak(subim2, 40*nSamp/2, 40*nSamp/2, range = 3*nSamp)
  corr = crosscorr(subim1, subim2 * c1[2]/c2[2], pmax, dxy, range = 5)
  dxy3 = normxcorr2(subim1, subim2, weight=submask)
  dc = c2 - c1
  print, dxy/10
  print, dc
  print, dxy3/10
  print, c1
  print, c2
;  subim2 = fshift(subim2, -dxy[0], -dxy[1])
  ;; c2 = findpeak(subim2, 41*nSamp/2, 41*nSamp/2, range = 3*nSamp)
  ;; print, c1
  ;; subim2 = subim2 * c1[2]/c2[2]
  ;; c2 = findpeak(subim2, 41*nSamp/2, 41*nSamp/2, range = 3*nSamp)
  ;; print, c2
END


