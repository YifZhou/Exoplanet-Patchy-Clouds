PRO residualError
  restore, '2015_Aug_26F125W_residual.sav'

  
  FOR i=0, 7 DO print, total(residual[*, *, i])
END
