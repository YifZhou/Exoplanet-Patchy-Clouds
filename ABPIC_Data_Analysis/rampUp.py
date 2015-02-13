from astropy.io import fits
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
from brewer2mpl import get_map

colors = get_map('Reds', 'Sequential', 9).mpl_colors[3:]
if __name__ == '__main__':
    dataDIR = '../data/ABPIC-B'
    x = int(sys.argv[1]) 
    y = int(sys.argv[2]) # do not use x or y, they are confusing
    dim1, dim2 = y, x
    fnList = sys.argv[3:]
    plt.close('all')
    for index, fn in enumerate(fnList):
        imaFn = fn + '_ima.fits'
        fltFn = fn + '_flt.fits'

        ima = fits.open(os.path.join(dataDIR, imaFn))
        flt = fits.open(os.path.join(dataDIR, fltFn))
        nSamp = ima['primary'].header['nsamp']
        count = np.zeros(nSamp)
        sampTime = np.zeros(nSamp)
        count[0] = ima['sci', nSamp].data[dim1, dim2]
        sampTime[0] = 0 # zeroth read
        for i, samp_i in enumerate(range(nSamp - 1, 0, -1)): #last samp is the first readout
            sampTime[i+1] = ima['sci', samp_i].header['samptime']
            print ima['sci', samp_i].data[dim1, dim2], ima['dq', samp_i].data[dim1, dim2]
            count[i+1] = ima['sci', samp_i].data[dim1, dim2] * sampTime[i + 1] + count[0]
        plt.plot(sampTime, count, marker = '+', ms = 12, color = colors[index])
        plt.plot(flt['primary'].header['exptime'], flt['sci'].data[dim1-5, dim2-5] * flt['primary'].header['exptime'] + count[0], 'o', ms = 12, color = colors[index])
        print sampTime, count
        print flt['sci'].data[dim1-5, dim2-5], flt['sci'].data[dim1-5, dim2-5] * flt['primary'].header['exptime'] + count[0]
        ima.close()
        flt.close()
    ax = plt.gca()
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Count (e$^-$)')

    plt.show()

    