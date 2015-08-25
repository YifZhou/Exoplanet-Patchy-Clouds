PRO residualError
  restore, 'F160W_residual.sav'

  
  FOR i=0, 7 DO print, total(residual[*, *, i])
END
