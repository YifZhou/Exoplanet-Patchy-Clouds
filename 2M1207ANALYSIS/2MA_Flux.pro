PRO Primary_Flux
  fn = '../data/2M1207B/'
  readcol, fn + 'flt_file_list.dat', fileList, filter, obsTime, format = 'a, x, x, a, x, a, x, x'
  nFiles = N_elements(fileList)
  x = fltarr(nFiles)
  y = fltarr(nFiles)
  flux = fltarr(nFiles)
  FOR i = 0, nFiles - 1 DO BEGIN
     im = mrdfits(fn + fileList[i], 1, hd, /silent)
     cen = findPeak(im, 141, 159, range = 20)
     aper, im, cen[0], cen[1], f, ef, sky, esky, 1., 5, [30, 50], [-100, 1e6], /silent, /flux
     x[i] = cen[0]
     y[i] = cen[1]
     flux[i] = f
  ENDFOR
  obstime = ' ' + obstime
  filter = ' ' + filter
  FORprint, fileList, flux, x, y, obstime, filter, textout = '2M1207A_flux_Dec4.dat', width = 160, /nocomment
END
