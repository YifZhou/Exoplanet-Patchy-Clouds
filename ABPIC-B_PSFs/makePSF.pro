FUNCTION makePSF, fn, dx, dy
  im = mrdfits(fn)
  im = fshift(im[1:270, 1:270], dx*10, dy*10)
  diffusion = [[0.0007, 0.025,  0.0007],$
               [0.0250, 0.897,  0.0250],$
               [0.0007, 0.025,  0.0007]]
  
  im0 = convol(binPSF(im), diffusion) ;;covolve with the diffusion kernel
  return, im0/total(im0) ;;normalize the psf
END

FUNCTION binPSF,psf
  binned = fltarr(27, 27)
  FOR i=0,26 DO BEGIN
     FOR j=0,26 DO BEGIN
        binned[i, j] = total(psf[10*i:10*i + 9, 10*j : 10*j+9])
     ENDFOR
  ENDFOR
  return, binned
END

