from astropy import wcs
from astropy.io import fits
import pandas as pd
from os import path
import numpy as np
import matplotlib.pyplot as plt

"""
Output the pointing shift measured by WCS coordinate
only for last three orbit
"""

if __name__ == '__main__':
    dataDIR = '../data/ABPIC-B'
    lon = 94.8099363233
    lat = -58.052184318
    df = pd.read_csv('2015_Feb_10_flt_aper=5_result.csv', parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    subdf = df[(df['ORBIT']<=12) & (df['ORBIT'] >=10)]
    dim1List = []
    dim2List = []
    for fn in subdf['FILENAME']:
        f = fits.open(path.join(dataDIR, fn))
        w = wcs.WCS(f['sci'].header)
        dim10, dim20 = w.wcs_world2pix(lon, lat, 1)
        dim1List.append(dim10)
        dim2List.append(dim20)
        f.close()

    subdf['HEADERX'] = dim2List
    subdf['HEADERY'] = dim1List
    subdf.to_csv('Orbit10to12HeaderPointing.csv')