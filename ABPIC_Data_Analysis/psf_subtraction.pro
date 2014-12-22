;+
; NAME:
;
;
;
; PURPOSE:
;
;
;
; CATEGORY:
;
;
;
; CALLING SEQUENCE:
;
;
;
; INPUTS:
;
;
;
; OPTIONAL INPUTS:
;
;
;
; KEYWORD PARAMETERS:
;
;
;
; OUTPUTS:
;
;
;
; OPTIONAL OUTPUTS:
;
;
;
; COMMON BLOCKS:
;
;
;
; SIDE EFFECTS:
;
;
;
; RESTRICTIONS:
;
;
;
; PROCEDURE:
;
;
;
; EXAMPLE:
;
;
;
; MODIFICATION HISTORY:
;
;-

FUNCTION fitPSF, id0, id_i, annulusIndex
  COMMON preparedData, cube, infoList, nImages, xMesh, yMesh
  c = 0.1 * findgen(20)
  residual = fltarr(n_elements(c))
  im0 = cube[*, *, id0]
  annulus0 = im0[annulusIndex]
  imi = cube[*, *, id_i]
  annulusi = imi[annulusIndex]
  FOR i = 0, 19 DO BEGIN
     residual[i] = total((annulus0 - c[i] * annulusi)^2)
  ENDFOR
  plot, c, residual
END


FUNCTION searchPSF, id0, satisfyID
  COMMON preparedData, cube, infoList, nImages, xMesh, yMesh
  nSatisfied = N_ELEMENTS(satisfyID)
  disPrimary = sqrt((xMesh - 127)^2 + (yMesh - 127)^2)
  IF infoList[id0].rollAngle EQ 101 THEN $
     gcntrd, cube[*, *, id0], 109., 166., xSecCen, ySecCen, 2.0 $
             ELSE gcntrd, cube[*, *, id0], 126., 172., xSecCen, ySecCen, 2.0
  disSecondary = sqrt((xMesh - xSecCen)^2 + (yMesh - ySecCen)^2)
  annulusPri = where((disPrimary GE 30) AND (disPrimary LE 60))
  annulusSec = where(disSecondary LE 15)
  annulusEff = cgsetdifference(annulusPri, annulusSec)
  c_fit = 0.99 + 0.002*findgen(11)
  c_int = congrid(c_fit, 200,/interp)
  residual = fltarr(n_elements(c_fit))
  cList = fltarr(nSatisfied)
  resList = fltarr(nSatisfied)
  skylevelList = fltarr(nSatisfied)
  skysigList = fltarr(nSatisfied)
  FOR i = 0, nSatisfied - 1  DO BEGIN
     id_i = satisfyID[i]
     IF infoList[id_i].rollAngle EQ 101 THEN $
     gcntrd, cube[*, *, id_i], 109., 166., xSecCen1, ySecCen1, 2.0 $ ;; find the center of the psf image
             ELSE gcntrd, cube[*, *, id_i], 126., 172., xSecCen1, ySecCen1, 2.0
     disRolled = sqrt((xMesh - xSecCen1)^2 + (yMesh - ySecCen1)^2)
     annulusRolled = where(disRolled LE 15)
     annulusEff_i0 = cgsetdifference(annulusEff, annulusRolled)
     sky, (cube[*,*,id0] - cube[*, *, id_i])[annulusEff_i0], mode, std, /silent
     annulusEff_i = annulusEff_i0[where(abs((cube[*,*,id0] - cube[*,*,id_i])[annulusEff_i0]) LE 3 *std)]
     print,n_elements(annulusEff_i0) - N_ELEMENTS(annulusEff_i), ' bad pixels excluded'
     FOR j = 0, n_elements(c_fit) -1 DO BEGIN
        resImage = cube[*,*,id0] - c_fit[j] * cube[*, *, id_i]
        residual[j] = sqrt(total(resImage[annulusEff_i]^2)/n_elements(annulusEff_i))
     ENDFOR
     res_int = interpol(residual, c_fit, c_int,/spline)
     cList[i]= mean(c_int[where(res_int EQ min(res_int))])
     resList[i] = min(res_int)
     sky, (cube[*,*,id0] - cList[i] * cube[*, *, id_i])[annulusEff_i0], mode, std
     skylevelList[i] = mode
     skysigList[i] = std
  ENDFOR
  minResId = where(resList EQ min(resList))
  psf_id = satisfyID[minResId]
  c0 = cList[minResId]
  skylevel = skylevelList[minResId]
  skysig = skysigList[minResId]
  return, [psf_id, c0, skylevel, skysig]                ; return psf id and c0
END

FUNCTION findPeak, im, x0, y0, range=range
  IF N_ELEMENTS(range) EQ 0 THEN range = 10
  xlow = floor(x0 - range)
  ylow = floor(y0 - range)
  yfit = mpfit2dpeak(im[xlow:xlow + 2*range, ylow:ylow+2*range], params, /moffat)
  return, [params[4] + xlow, params[5] + ylow]
END

FUNCTION searchPSF2, id0, satisfyID
  ;; deal with the unaligned prepared images
  COMMON preparedData, cube, infoList, nImages, xMesh, yMesh
  dx = infoList.xCenter - infoList[id0].xCenter
  dy = infoList.yCenter - infoList[id0].yCenter
  dx_frac = (abs(dx - round(dx)))[satisfyID]
  dy_frac = (abs(dy - round(dy)))[satisfyID]  ;; only consider satisfied
  satisfyID = satisfyID[(sort(dx_frac^2 + dy_frac^2))[0:4]] ;; choose PSF that has the smallest fractional shift
  nSatisfied = N_ELEMENTS(satisfyID)
  disPrimary = sqrt((xMesh - 127)^2 + (yMesh - 127)^2)
  secCen1 = [109., 166.]
  secCen2 = [126., 172.]
  dx0 = infoList[id0].xCenter - 127
  dy0 = InfoList[id0].yCenter - 127
  image0 = cube[*, *, id0]
  IF infoList[id0].rollAngle EQ 101 THEN $
     secCen = findPeak(image0, secCen1[0] + dx0, secCen1[1] + dy0, range = 5) $
  ELSE secCen = findPeak(image0, secCen2[0] + dx0, secCen2[1] + dy0, range = 5)
  disSecondary = sqrt((xMesh - secCen[0])^2 + (yMesh - secCen[1])^2)
  annulusPri = where((disPrimary GE 30) AND (disPrimary LE 60))
  annulusSec = where(disSecondary LE 15)
  annulusEff = cgsetdifference(annulusPri, annulusSec)
  c_fit = 0.99 + 0.002*findgen(11)
  c_int = congrid(c_fit, 200,/interp)
  residual = fltarr(n_elements(c_fit))
  cList = fltarr(nSatisfied)
  resList = fltarr(nSatisfied)
  skylevelList = fltarr(nSatisfied)
  skysigList = fltarr(nSatisfied)
  FOR i = 0, nSatisfied - 1  DO BEGIN
     id_i = satisfyID[i]
     image_i = fshift(cube[*, *, id_i], -dx[id_i], -dy[id_i])
     IF infoList[id_i].rollAngle EQ 101 THEN $
        secCen_i = findPeak(image_i, secCen1[0] + dx0, secCen1[1] + dy0, range = 5) $
     ELSE secCen_i = findPeak(image_i, secCen2[0] + dx0, secCen2[1] + dy0, range = 5)

     disRolled = sqrt((xMesh - SecCen_i[0])^2 + (yMesh - SecCen_i[1])^2)
     annulusRolled = where(disRolled LE 15)
     annulusEff_i0 = cgsetdifference(annulusEff, annulusRolled)
     sky, (image0 - image_i)[annulusEff_i0], mode, std, /silent
     annulusEff_i = annulusEff_i0[where(abs((image0 - image_i)[annulusEff_i0]) LE 3 *std)]
     print,n_elements(annulusEff_i0) - N_ELEMENTS(annulusEff_i), ' bad pixels excluded'
     FOR j = 0, n_elements(c_fit) -1 DO BEGIN
        resImage = image0 - c_fit[j] * image_i
        residual[j] = sqrt(total(resImage[annulusEff_i]^2)/n_elements(annulusEff_i))
     ENDFOR
     res_int = interpol(residual, c_fit, c_int,/spline)
     cList[i]= mean(c_int[where(res_int EQ min(res_int))])
     resList[i] = min(res_int)
     sky, (image0 - cList[i] * image_i)[annulusEff_i0], mode, std
     skylevelList[i] = mode
     skysigList[i] = std
  ENDFOR
  minResId = where(resList EQ min(resList))
  psf_id = satisfyID[minResId]
  c0 = cList[minResId]
  skylevel = skylevelList[minResId]
  skysig = skysigList[minResId]
  xshift = dx[psf_id]
  yshift = dy[psf_id]
  return, [psf_id, c0, skylevel, skysig, secCen[0], secCen[1], xshift, yshift] ; return psf id and c0
END


PRO psf_subtraction, input_fn, output_fn
  COMMON preparedData, cube, infoList, nImages, xMesh, yMesh
  restore, input_fn ;; restore data from data preparation PROCEDURE
  cube1 = cube
  infoList1 = REPLICATE(create_struct(infoList[0], 'PSF_id', 0, 'PSF_amplitude', 0.0, 'skyLevel', 0.0, 'skySigma', 0.0, 'xCenter_sec', 0.0, 'yCenter_sec', 0.0), N_ELEMENTS(infoList))
  szCube = size(cube)
  nImages = szCube[3]
  meshgrid, findgen(256), findgen(256), xMesh, yMesh
  FOR i = 0, nImages - 1 DO BEGIN
     angle_i = infoList[i].rollAngle
     filter_i = infoList[i].filter
     satisfyID = where((infoList.filter EQ filter_i) AND (infoList.rollAngle NE angle_i))
     fitResult = searchPSF2(i, satisfyID)
     infoList1[i].filter = infoList[i].filter 
     infoList1[i].exposureTime = infoList[i].exposureTime
     infoList1[i].obsDate = infoList[i].obsDate
     infoList1[i].obsTime = infoList[i].obsTime
     infoList1[i].orbit = infoList[i].orbit
     infoList1[i].dither = infoList[i].dither
     ;; infoList1[i].xShift = infoList[i].xShift
     ;; infoList1[i].yShift = infoList[i].yShift
     infoList1[i].xCenter = infoList[i].xCenter
     infoList1[i].yCenter = infoList[i].yCenter
     infoList1[i].PSF_id = fitResult[0]
     infoList1[i].PSF_amplitude = fitResult[1]
     infoList1[i].skyLevel = fitResult[2]
     infoList1[i].skySigma = fitResult[3]
     infoList1[i].xCenter_sec = fitResult[4]
     infoList1[i].yCenter_sec = fitResult[5]
     infoList1[i].rollAngle = infoList[i].rollAngle
     cube1[*, *, i] = cube[*, *, i] - fitResult[1] * fshift(cube[*, *, fitResult[0]], -fitResult[6], -fitResult[7])
  ENDFOR
  save, cube1, infoList1, filename = output_fn
END

