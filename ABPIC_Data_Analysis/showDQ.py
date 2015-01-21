import numpy as np
from astropy.io import fits
import sys
import matplotlib.pyplot as plt
import pandas as pd

def dq2Bad(dq, flag):
    dqbin = ['{0:016b}'.format(i) for i in dq.flat]
    isBad = np.array([True if dqstr[-flag] == '1' else False for dqstr in dqbin]).reshape(np.shape(dq))
    return isBad

if __name__ == '__main__':
    DF = pd.read_csv('ABPIC-B_fileInfo.csv')
    fitsFileList = DF['file name']
    concernedFlag = [3, 5, 6, 7, 13, 14]
    markers = ['x', '+', '.', 's', '3', '4']
    for fitsfn in fitsFileList:
        fitsContent = fits.open('../data/ABPIC-B/' + fitsfn)
        im = fitsContent['SCI'].data
        dq = fitsContent['DQ'].data
        fig, ax = plt.subplots()

        ax.imshow(np.arcsinh(im), cmap = 'hot', interpolation = 'nearest')


        for i, flag in enumerate(concernedFlag):
            badPixelMap = dq2Bad(dq, flag)
            x, y = np.where(badPixelMap)
            print len(x)
            ax.plot(y, x, linewidth = 0, marker = markers[i], ms = 4)

        figName = fitsfn.replace('.fits', '_dq.pdf')
        fig.savefig('./dq/' + figName)
        print figName, ' saved'
        plt.close(fig)
        fitsContent.close()
    