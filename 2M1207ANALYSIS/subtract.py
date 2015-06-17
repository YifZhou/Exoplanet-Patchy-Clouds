#! /usr/bin/env python
from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from astropy.io import fits
import pandas as pd
from scipy.ndimage.interpolation import shift

"""using observed PSF to do subtraction
"""


def subtraction(im1, im2, dxy1, dxy2):
    """
    Keyword Arguments:
    im1  -- first image
    im2  -- second image
    dxy1 -- movement of first image
    dxy2 -- movement of second image
    """
    pass

if __name__ == '__main__':
    df = pd.read_csv('2015_Jun_15TinyTimF125Result.csv',
                     parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
                     index_col='datetime')
    dataDIR = '../data/2M1207B/'
    subdf1 = df[df['ORBIT'] == 1]
    subdf2 = df[df['ORBIT'] == 2]
    im1 = fits.getdata(dataDIR + subdf1['FILENAME'].values[0], 1)
    err1 = fits.getdata(dataDIR + subdf1['FILENAME'].values[0], 2)
    im2 = fits.getdata(dataDIR + subdf2['FILENAME'].values[0], 1)
    err2 = fits.getdata(dataDIR + subdf2['FILENAME'].values[0], 2)
    cxy1 = np.array([subdf1['PRIMARY_X'].values[0],
                     subdf1['PRIMARY_Y'].values[0]])
    cxy2 = np.array([subdf2['PRIMARY_X'].values[0],
                     subdf2['PRIMARY_Y'].values[0]])
    amp1 = subdf1['FLUXA'].values[0]
    amp2 = subdf2['FLUXA'].values[0]
    dxy1 = cxy1 - np.floor(cxy1)
    dxy2 = cxy2 - np.floor(cxy2)
    dxy = dxy1 - dxy2

    subim1 = im1[np.floor(cxy1[1]) - 13: np.floor(cxy1[1]) + 13,
                 np.floor(cxy1[0]) - 13: np.floor(cxy1[0]) + 13]
    subim2 = im2[np.floor(cxy2[1]) - 13: np.floor(cxy2[1]) + 13,
                 np.floor(cxy2[0]) - 13: np.floor(cxy2[0]) + 13]

    # shift the image
    subim1 = shift(subim1, dxy / 2)
    subim2 = shift(subim2, -dxy / 2)
    plt.close('all')
    fig = plt.figure()
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)

    diff = subim1 - amp2 / amp1 * subim2
    ax1.imshow(np.arcsinh(subim1), interpolation='nearest')
    ax2.imshow(np.arcsinh(subim2), interpolation='nearest')
    ax3.imshow(diff, vmin=-10, vmax=10, interpolation='nearest')
    plt.show()
