#! /usr/bin/env python
import sys
import matplotlib.pyplot as plt
import pandas as pd
from astropy.io import fits
import numpy as np
from brewer2mpl import get_map
colors = get_map('Set1', 'Qualitative', 4).mpl_colors


if __name__ == '__main__':
    DF = pd.read_csv('2457042_ima_aper=5_result.csv', parse_dates = {'datetime': ['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    plt.close('all')
    fig = plt.figure(figsize = (6,8))
    ax125 = fig.add_subplot(211)
    ax160 = fig.add_subplot(212)
    for filt, ax, thres in zip(['F125W', 'F160W'], [ax125, ax160], [800, 1500]):
        for index, orbit in enumerate([10, 11, 12]):
            subFrame = DF[(DF['FILTER'] == filt) & (DF['ORBIT'] == orbit)]
            if not subFrame.empty:
                ax.plot(subFrame.index, subFrame['YCENTER'] - subFrame['YCENTER'].values[0], '.', color = colors[0])
                ax.plot(subFrame.index, subFrame['XCENTER'] - subFrame['XCENTER'].values[0], '+', color = colors[1])

    for ax in [ax125, ax160]:
        ax.set_ylabel('Center')
        ax.set_xlabel('UT')

    ax125.set_title('F125W')
    ax160.set_title('F160W')
    fig.autofmt_xdate()
    fig.savefig('Ymove.pdf')
    plt.show()
    