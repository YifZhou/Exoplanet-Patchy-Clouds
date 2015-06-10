from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
def readPSF(fn):
    im = fits.getdata(fn, 0)
    psf = fits.getdata(fn, 1)
    return im - psf




df = pd.read_csv('TinyTimF125Result.csv', parse_dates = {'datetime':['OBSDATE', 'OBSTIME']}, index_col = 'datetime')
fnList = df['FILENAME'].values
for i in range(len(fnList)):
    fnList[i] = 'i'+ fnList[i].strip('_flt.fits')

for i in range(len(fnList)):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    psf = np.arcsinh(readPSF('./fitsResult/' + fnList[i] +'.fits'))
    ax.imshow(psf, interpolation = 'nearest')
    ax.set_title('dither = {0}, angle = {1}'.format(df['DITHER'][i], df['POSANGLE'][i]))
    plt.savefig('./F125DIFF/' + fnList[i] + '.pdf')


