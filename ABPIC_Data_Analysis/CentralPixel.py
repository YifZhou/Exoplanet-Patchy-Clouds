#! /usr/bin/env python
"""
check if there is significant ramp effect
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
from brewer2mpl import get_map
from astropy.io import fits
import numpy as np
colors = get_map('Set1', 'Qualitative', 4).mpl_colors

dim10 = 227
dim20 = 134
def centralValue(dim1, dim2, fn, side = 0):
    im = fits.open(fn)['sci', 1].data
    return np.sum(im[dim1 - side: dim1 + side + 1, dim2 - side: dim2 + side + 1])

if __name__ == '__main__':
    orbit = 12
    filter = 'F160W'
    dataDIR = '../data/ABPIC-B/'
    df = pd.read_csv('2015_Feb_10_ima_aper=5_result.csv', parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    subdf = df[(df['FILTER'] == filter) & (df['ORBIT'] == orbit)]
    count00 = []
    countx0 = []
    count0x = []
    county0 = []
    count0y = []
    count3x3 = []
    for fn in subdf['FILENAME']:
        count00.append(centralValue(dim10, dim20, os.path.join(dataDIR, fn), side = 0))
        countx0.append(centralValue(dim10, dim20 - 1, os.path.join(dataDIR, fn), side = 0))
        count0x.append(centralValue(dim10, dim20 + 1, os.path.join(dataDIR, fn), side = 0))
        county0.append(centralValue(dim10 - 1, dim20, os.path.join( dataDIR, fn), side = 0))
        count0y.append(centralValue(dim10 + 1, dim20, os.path.join(dataDIR, fn), side = 0))
        count3x3.append(centralValue(dim10, dim20, os.path.join(dataDIR, fn), side = 1))

    count00 = np.array(count00)
    count3x3 = np.array(count3x3)
    countx0 = np.array(countx0)
    count0x = np.array(count0x)
    county0 = np.array(county0)
    count0y = np.array(count0y)
    plt.close('all')
    plt.plot(subdf.index, count00/np.max(count00), label = 'original', linewidth = 3)
    plt.plot(subdf.index, countx0/np.max(countx0), label = 'x-1, y')
    plt.plot(subdf.index, count0x/np.max(count0x), label = 'x+1, y')
    plt.plot(subdf.index, county0/np.max(county0), label = 'x, y-1')
    plt.plot(subdf.index, count0y/np.max(count0y), label = 'x, y+1', linewidth = 3)
    plt.plot(subdf.index, count3x3/np.max(count3x3), label = '3x3 square', color = 'k', linewidth = 3)
    plt.gcf().autofmt_xdate()
    plt.legend(loc = 'best')
    plt.xlabel('UT')
    plt.ylabel('Normalized Flux')
    plt.savefig('CentralPixelTrend_orbit{0}_F160W.pdf'.format(orbit))