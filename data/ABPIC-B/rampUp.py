#! /usr/bin/env python
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import sys

if __name__ == '__main__':
    fnList = [fn + '_ima.fits' for fn in sys.argv[1:]]
    index = range(1,7)
    flux = []
    center = [135, 227]
    fig, ax = plt.subplots()
    for fn in fnList:
        fitsContent = fits.open(fn)
        flux[:] = []
        for i in index:
            im = fitsContent['sci', i].data
            flux.append(np.sum(im[center[1] -6: center[1] + 6, center[0] -6: center[0] + 6]))

        ax.plot(index, np.array(flux[::-1]), marker = 'x')
        print fn, ':', flux[::-1]    
        
    plt.show()