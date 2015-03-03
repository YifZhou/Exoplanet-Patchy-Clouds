from astropy import wcs
from astropy.io import fits
import pandas as pd
from os import path
import numpy as np
import matplotlib.pyplot as plt

"""
plot the flux for one pixel as a function of the pointing shift
and show the trend
"""

if __name__ == '__main__':
    orbit = 12
    filter = 'F160W'
    dataDIR = '../data/ABPIC-B'
    dim1 = 222
    dim2 = 129 #record the wcs of the peak pixel
    df = pd.read_csv('2015_Feb_10_flt_aper=5_result.csv', parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    subdf = df[(df['FILTER'] == filter) & (df['ORBIT'] == orbit)]
    f = fits.open(path.join(dataDIR, subdf['FILENAME'].values[0]))
    
    w = wcs.WCS(f['sci'].header)
    lon, lat = w.wcs_pix2world(dim1, dim2, 1)
    f.close()
    dim1List = []
    dim2List = []
    cvalue = []
    for fn in subdf['FILENAME']:
        f = fits.open(path.join(dataDIR, fn))
        w = wcs.WCS(f['sci'].header)
        dim10, dim20 = w.wcs_world2pix(lon, lat, 1)
        dim1List.append(dim10)
        dim2List.append(dim20)
        cvalue.append(f['sci'].data[dim1, dim2])
        f.close()

    dim1List = np.array(dim1List)
    dim2List = np.array(dim2List)
    plt.plot(dim1List - dim1List[0], cvalue, '-o', label = 'x shift')
    #plt.plot(subdf.index, dim1List - dim1List[0], '-+', label = 'y shift')
    # plt.xlabel('UT')
    # plt.ylabel('$\Delta$ (pixel)')
    plt.xlabel('$\Delta$ (pixel)')
    plt.ylabel('flux')
    fig = plt.gcf()
    fig.autofmt_xdate()
    plt.show()
