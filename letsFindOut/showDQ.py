import numpy as np
from astropy.io import fits
import sys
import matplotlib.pyplot as plt

def dq2Bad(dq, flag):
    dqbin = ['{0:016b}'.format(i) for i in dq.flat]
    isBad = np.array([True if dqstr[-flag] == '1' else False for dqstr in dqbin]).reshape(np.shape(dq))
    return isBad

if __name__ == '__main__':
    fitsContent = fits.open(sys.argv[1])
    im = fitsContent['SCI'].data
    dq = fitsContent['DQ'].data
    concernedFlag = [3, 5, 6, 13]
    fig, ax = plt.subplots()
    
    ax.imshow(np.arcsinh(im), cmap = 'hot', interpolation = 'nearest')
    

    for flag in concernedFlag:
        badPixelMap = dq2Bad(dq, flag)
        x, y = np.where(badPixelMap)
        print len(x)
        ax.plot(x, y, marker = '${0}$'.format(flag), linewidth = 0)

    plt.show()
    