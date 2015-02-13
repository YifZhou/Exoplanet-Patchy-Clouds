from astropy.io import fits
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
from brewer2mpl import get_map
from scipy.optimize import curve_fit

def plotRamp (ax, sampTime, count, fltCount, color):
    """
    plot ramp up
    """
    def func(x, *p):
        return x * p[0] + p[1]
    paras, pcov = curve_fit(func, sampTime, count, p0 = [(count[-1] - count[0])/sampTime[-1], count[0]], sigma = np.sqrt(np.abs(count)), absolute_sigma = True)

    ax.errorbar(sampTime, count, yerr = np.sqrt(np.abs(count)), fmt = 'o', color = color)
    ax.plot(sampTime, sampTime * paras[0] + paras[1], color = color, ms = 12)
    ax.plot(sampTime[-1], fltCount, 'x', color = color, ms = 12)
    print 'fltCount: {0},\n fitCount: {1}'.format((fltCount - count[0])/sampTime[-1], paras[0])

colors = get_map('Set1', 'Qualitative', 9).mpl_colors
if __name__ == '__main__':
    dataDIR = '../data/ABPIC-B'
    x = int(sys.argv[1]) 
    y = int(sys.argv[2]) # do not use x or y, they are confusing
    dim1, dim2 = y, x
    fnList = sys.argv[3:]
    plt.close('all')
    fig, ax = plt.subplots()
    for index, fn in enumerate(fnList):
        print 'Filename: {0}'.format(fn)
        imaFn = fn + '_ima.fits'
        fltFn = fn + '_flt.fits'

        ima = fits.open(os.path.join(dataDIR, imaFn))
        flt = fits.open(os.path.join(dataDIR, fltFn))
        nSamp = ima['primary'].header['nsamp']
        count = np.zeros(nSamp -1)
        sampTime = np.zeros(nSamp - 1)
        # count[0] = ima['sci', nSamp].data[dim1, dim2]
        # sampTime[0] = 0 # zeroth read
        print 'Value', 'Flag'
        for i, samp_i in enumerate(range(nSamp - 1, 0, -1)): #last samp is the first readout
            sampTime[i] = ima['sci', samp_i].header['samptime']
            print ima['sci', samp_i].data[dim1, dim2], ima['dq', samp_i].data[dim1, dim2]
            count[i] = ima['sci', samp_i].data[dim1, dim2] * sampTime[i] #+ count[0]


        plotRamp(ax, sampTime, count, count[0] + flt['sci'].data[dim1 - 5, dim2 - 5] * flt['primary'].header['exptime'], colors[index])
        ima.close()
        flt.close()
        print '*****\n'
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Count (e$^-$)')

    plt.show()

    