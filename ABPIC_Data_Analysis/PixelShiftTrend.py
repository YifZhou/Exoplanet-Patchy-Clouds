#! /usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys, glob
from os import path
sys.path.append('../python_src')
from ExposureSet import ExposureSet
from linearFit import linearFit

def plotTrend (dataStack, xCenter, side = 2, output = None):#2side+1 x 2side+1 pixels subimage
    plt.close('all')
    fig, axes = plt.subplots(ncols = 2*side + 1, nrows = 2*side + 1, sharex = True, sharey = True, figsize = (24, 20))
    fig.subplots_adjust(hspace = 0, wspace = 0)
    subIMShape = dataStack.shape
    c = subIMShape[0]//2
    delta = xCenter - xCenter[0]
    for i, dim0 in enumerate(range(c-side, c+side+1)):
        for j, dim1 in enumerate(range(c-side, c+side+1)):
            y = dataStack[dim0, dim1, :]/dataStack[dim0, dim1, :].mean()
            err = np.sqrt(np.abs(dataStack[dim0, dim1, :]))/np.abs(dataStack[dim0, dim1, :])#relative uncertainty
            b, m, db, dm, chisq = linearFit(delta, y, y*err)
            axes[i, j].plot(delta, y, linewidth = 0, marker = '.', label = '({0}, {1})')
            axes[i, j].plot(np.sort(delta), np.sort(delta)*m + b)
            axes[i, j].annotate('x={0},y={1}'.format(dim1 - c, dim0 - c), xy = (0.2, 0.8), xycoords = 'axes fraction')
            axes[i, j].xaxis.set_major_locator(plt.MaxNLocator(4))

    if output is None:
        plt.show()
    else:
        plt.savefig(output)
            
if __name__ == '__main__':
    infoDF = pd.read_csv('Orbit10to12HeaderPointing.csv', parse_dates = 'datetime', index_col = 'datetime')
    dataDIR = '../data/ABPIC-B_myfits/'
    pixelCount125 = np.zeros((11, 11, 28, 3))
    pixelCount160 = np.zeros((11, 11, 30, 3))
    expTime = 30.0
    
    for orbitIndex, orbit in enumerate([10, 11, 12]):
        expID125 = iter(range(28))
        expID160 = iter(range(30))
        for expFN in sorted(glob.glob(path.join(dataDIR ,'Orbit{0}*expSet.pkl'.format(orbit)))):
            expSet = ExposureSet.load(expFN)
            if expSet.filterName == 'F125W':
                for HSTFile in expSet.HSTFileList:
                    pixelCount125[:, :, next(expID125), orbitIndex] = HSTFile.fitCountArray
            elif expSet.filterName == 'F160W':
                for HSTFile in expSet.HSTFileList:
                    pixelCount160[:, :, next(expID160), orbitIndex] = HSTFile.fitCountArray
            else:
                pass
    ###### do the plot######
    #for orbit in [10, 11, 12]:
    #     for direction in ['X', 'Y']:
    #         outfn = 'PixelTrend_{0}_{1}_Header{2}.pdf'.format('F125W',orbit, direction)
    #         plotTrend(pixelCount125[:,:,:,orbit-10]*expTime, infoDF[(infoDF['FILTER'] == 'F125W') & (infoDF['ORBIT'] == orbit)]['HEADER' + direction].values, side = 2, output = outfn)
    #         print outfn, 'plotted'

    # for orbit in [10, 11, 12]:
    #     for direction in ['X', 'Y']:
    #         outfn = 'PixelTrend_{0}_{1}_Header{2}.pdf'.format('F160W',orbit, direction)
    #         plotTrend(pixelCount160[:,:,:,orbit-10]*expTime, infoDF[(infoDF['FILTER'] == 'F160W') & (infoDF['ORBIT'] == orbit)]['HEADER' + direction].values, side = 2, output = outfn)
    #         print outfn, 'plotted'

    ##plot against time

    for orbit in [10, 11, 12]:
        outfn = 'PixelTrendvsTime_{0}_{1}.pdf'.format('F125W', orbit)
        time = infoDF[(infoDF['FILTER'] == 'F125W') & (infoDF['ORBIT'] == orbit)].index
        time = time.day*24*60.0 + time.hour * 60.0 + time.minute + time.second/60.0
        plotTrend(pixelCount125[:,:,:,orbit-10]*expTime, time, side = 2, output = outfn)

    for orbit in [10, 11, 12]:
        outfn = 'PixelTrendvsTime_{0}_{1}.pdf'.format('F160W', orbit)
        time = infoDF[(infoDF['FILTER'] == 'F160W') & (infoDF['ORBIT'] == orbit)].index
        time = time.day*24*60.0 + time.hour * 60.0 + time.minute + time.second/60.0
        plotTrend(pixelCount160[:,:,:,orbit-10]*expTime, time, side = 2, output = outfn)

    
    
