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
    bins = np.linspace(0.77, 0.79, 10)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
    axes = [ax1, ax2, ax3, ax4]
    for i, ax in enumerate(axes):
        ax.hist(dr[df125['DITHER'] == i].values, bins)
        ax.set_xlabel('Separation')
        ax.set_ylabel('n')
        ax.set_title('Dither {0}'.format(i))

    fig.tight_layout()
    plt.show()

        
    

