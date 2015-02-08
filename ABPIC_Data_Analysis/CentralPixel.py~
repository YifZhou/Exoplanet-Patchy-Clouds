#! /usr/bin/env python
"""
check if there is significant ramp effect
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from brewer2mpl import get_map
from astropy.io import fits
colors = get_map('Set1', 'Qualitative', 4).mpl_colors

def plotCentralPixel (ax, DF, thres):
    """
    plot central value, show if it has ramp effect
    """
    centralFlux = []
    for index, row in DF.iterrows():
        fitsFile = fits.open('../data/ABPIC-B/' + row['FILENAME'].values)
        yc, xc = row['XCENTER'].values, row['YCENTER'].values
        print fitsFile['SCI', 1].data[xc, yc]
        #centralFlux.append(fitsFile['SCI', 1].data[])
    
if __name__ == '__main__':
    DF = pd.read_csv('2457042_ima_aper=5_result.csv', parse_dates = {'datetime': ['OBS_DATE', 'OBS_TIME']}, index = 'datetime')
    fig = plt.figure(figsize = (6,8))
    ax125 = fig.add_subplot(211)
    ax160 = fig.add_subplot(212)
    for filt, ax, thres in zip(['F125W', 'F160W'], [ax125, ax160]), [800, 1500]:
        for orbit in range(6, 13):
            for exposure in range(0, 13):
                subFrame = DF[(DF['FILTER'] == filt) & (DF['ORBIT'] == orbit)
                              & (DF['EXPOSURE'] == exposure)]
                plotCentralPixel(ax, subFrame, thres)