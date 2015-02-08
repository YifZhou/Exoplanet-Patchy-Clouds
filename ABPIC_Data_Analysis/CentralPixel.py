#! /usr/bin/env python
"""
check if there is significant ramp effect
"""
import pandas as pd
import sys
import matplotlib.pyplot as plt
from brewer2mpl import get_map
from astropy.io import fits
import numpy as np
colors = get_map('Set1', 'Qualitative', 4).mpl_colors

def plotCentralPixel (ax, DF, nPixel = 1):
    """
    plot central value, show if it has ramp effect
    """
    centralFlux = pd.Series(dtype = float, index = DF.index)
    dither = DF['DITHER'].values[0]
    for index, row in DF.iterrows():
        fitsFile = fits.open('../data/ABPIC-B/' + row['FILENAME'])
        yc, xc = round(row['XCENTER']), round(row['YCENTER'])
        centralFlux[index] = np.sort(fitsFile['SCI', 1].data[xc-2: xc + 2, yc - 2: yc + 2].flat)[-1:-1-nPixel:-1].sum()
    ax.plot(DF.index, centralFlux * DF['EXPOSURE_TIME'], marker = '.', color = colors[dither])
    
if __name__ == '__main__':
    plotFn = sys.argv[1]
    nPixel = int(sys.argv[2])
    DF = pd.read_csv('2457042_ima_aper=5_result.csv', parse_dates = {'datetime': ['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    plt.close('all')
    fig = plt.figure(figsize = (6,8))
    ax125 = fig.add_subplot(211)
    ax160 = fig.add_subplot(212)
    for filt, ax, thres in zip(['F125W', 'F160W'], [ax125, ax160], [800, 1500]):
        for orbit in range(6, 13):
            for exposure in range(0, 13):
                subFrame = DF[(DF['FILTER'] == filt) & (DF['ORBIT'] == orbit)
                              & (DF['EXPOSURE_SET'] == exposure)]
                if not subFrame.empty: plotCentralPixel(ax, subFrame, nPixel = nPixel)

    for ax in [ax125, ax160]:
        ax.set_ylabel('Counts (e$^-$)')
        ax.set_xlabel('UT')

    ax125.set_title('F125W, maximum {0} pixel(s)'.format(nPixel))
    ax160.set_title('F160W, maximum {0} pixel(s)'.format(nPixel))
    fig.autofmt_xdate()
    fig.savefig(plotFn)
    plt.show()
    