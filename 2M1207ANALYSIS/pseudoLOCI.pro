FUNCTION maskoutdq, dq, flagList=flaglist
  IF N_elements(flagList) EQ 0 THEN flagList = [8, 32, 512]
  dq = long(dq)
  mask = dq-dq+1 ;;initialize mask
  FOR k=0, n_elements(flagList) - 1 DO BEGIN
     mask = mask * (1- dq/flagList[k] MOD 2)
  ENDFOR 
  return, mask
END

FUNCTION shiftMask, mask, dx, dy
  invMask = fshift(1-mask, dx, dy)
  invMask[where(invMask NE 0)] = 1 ;; pixel contaminated by hot pixel during shift is masked out.
  return, 1-invMask
END

PRO pseudoLOCI, PSFList
  imageFN = 'PSFCUBE_F125W.sav'
  restore, imageFN
  i = 0
  image_i = image125[i].image
  mask_i = maskoutdq(image125[i].dq)
  fixpix, image_i, mask_i, image_fixed ;;fix bad pixels
  image_i_int = congrid(image_fixed, 10*51, 10*51, cubic = -0.5, /minus_one)
  
  satisfiedPSF = where(PSF125.rollAngle NE image125[i].rollAngle)
  PSFList = make_array(510, 510, n_elements(satisfiedPSF), /float, value = 0) ;; array for save displacement
  PSFMaskList = make_array(510, 510, n_elements(satisfiedPSF), /float, value = 0)
  cube = fltarr(510, 510, 4)
  xy0 = findpeak(image_i_int, 255, 255, range=20)
  FOR j=0, n_elements(satisfiedPSF) - 1 DO BEGIN     
     mask_j = maskoutdq(PSF125[satisfiedPSF[j]].dq)
     fixpix, PSF125[satisfiedPSF[j]].image, mask_j, psf_fixed
     PSF_int =  congrid(psf_fixed, 10*51, 10*51, cubic = -0.5, /minus_one)
     mask = make_mask(fltarr(510, 510)+1, [[295, 225, 0, 50], [255,255, 200, 1000]]) ;; uncomment
     ;; this line when normalzied cross correlation is working

     
;;     dxy_ij = normxcorr2(image_i_int, PSF_int, weight = mask)
     corr = crosscorr(image_i_int, PSF_int, pmax, dxy)
;;     xy_ij = findpeak(PSF_int, 255, 255, range= 20)
;;     dxy3 = xy_ij-xy0
     ;; dirty trick, the masked cross correlation really needs to be
     ;; figure out
     ;; here, to avoid the contamination from companion object and a
     ;; clear comtamination from a hot pixel, only use the left side
     ;; of the image to do cross correlation.
;;     print, dxy_ij
;;     print, dxy
;;     print, dxy3
     ;; cube[*,*,0] = image_i_int
     ;; cube[*,*,1] = 7.5*fshift(PSF_int, -dxy_ij[0], -dxy_ij[1])
     ;; cube[*,*,2] = 7.5*fshift(PSF_int, -dxy[0], -dxy[1])
     ;; cube[*,*,3] = 7.5*fshift(PSF_int, -dxy3[0], -dxy3[1])
     PSFList[*, *, j] = fshift(PSF_int, -dxy[0], -dxy[1])
  endfor
  ;; use chisq to select the best PSF
  chisqList  = fltarr((size(PSFMaskList))[3])
  coeffList = fltarr((size(PSFMaskList))[3])
  FOR j = 0, (size(PSFMaskList))[3] - 1 DO BEGIN
     mask = make_mask(fltarr(510,510)+1, [[255, 255, 150, 1000], [295, 225, 0, 50]])
     coeffList[j] = total(mask*image_i_int * PSFList[*, *, j])/total((mask * PSFList[*, *, j])^2)
     chisqList[j] = total((mask * (image_i_int - coeffList[j]*PSFList[*, *, j]))^2)
  ENDFOR
  psf_id = where(chisqList EQ min(chisqList))
  print, psf_id
  stop
END

  


