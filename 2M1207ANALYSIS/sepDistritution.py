#! /usr/bin/env python
from __future__ import print_function, division
import numpy as  np
import matplotlib.pyplot as plt
import pandas as pd
plt.style.use('ggplot')
"""plot seperation distribution
"""

if __name__ == '__main__':
    xscale = 0.135 #arcsec/pixel
    yscale = 0.121 #arcsec/pixel
    fn125 = 'TinyTimF125Result.csv'
    fn160 = 'TinyTimF160Result.csv'
    df125 = pd.read_csv(fn125, parse_dates = {'datetime':['OBSDATE', 'OBSTIME']}, index_col = 'datetime')
    df160 = pd.read_csv(fn160, parse_dates = {'datetime':['OBSDATE', 'OBSTIME']}, index_col = 'datetime')
    dx = df125['PRIMARY_X'] - df125['SECONDARY_X']
    dy = df125['PRIMARY_Y'] - df125['SECONDARY_Y']
    dr = np.sqrt((dx*xscale)**2 + (dy*yscale)**2)
    plt.hist(dr)
    plt.show()