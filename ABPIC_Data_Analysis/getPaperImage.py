import idlsave
from astropy.io import fits
cube =idlsave.read('2015_May_07_prepared.sav')
cube1 = idlsave.read('2015_May_07_subtracted.sav')

fitsFN = '../data/ABPIC-B/icdg07p3q_flt.fits'
primaryHD = fits.getheader(fitsFN, 'primary')
sciHD = fits.getheader(fitsFN, 'sci')

fits1 = fits.HDUList([fits.PrimaryHDU(header = primaryHD), fits.ImageHDU(cube.cube[0, :, :], header = sciHD)])
fits2 = fits.HDUList([fits.PrimaryHDU(header = primaryHD), fits.ImageHDU(cube1.cube1[0, :, :], header = sciHD)])

fits1.writeto('original.fits', clobber = True)
fits2.writeto('subtracted.fits', clobber = True)