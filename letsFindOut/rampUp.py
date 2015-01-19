import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

if __name__ == '__main__':
#    fnList = ['icdg10v9q_ima.fits', 'icdg10vaq_ima.fits', 'icdg10vbq_ima.fits', 'icdg10vcq_ima.fits']
    fnList = ['icdg10v8q_ima.fits']
    #index = range(1,7)
    index = range(1,5)
    flux = []
    center = [135, 227]
    fig, ax = plt.subplots()
    for fn in fnList:
        fitsContent = fits.open(fn)
        flux[:] = []
        for i in index:
            im = fitsContent['sci', i].data
            hd = fitsContent['sci', i].header
            print  hd['SAMPNUM'], hd['SAMPTIME'], hd['DELTATIM']
            flux.append(np.sum(im[center[1] -6: center[1] + 6, center[0] -6: center[0] + 6]))

        ax.plot(index, np.array(flux[::-1]), marker = 'x')
        print fn, ':', flux[::-1]
        
    plt.show()