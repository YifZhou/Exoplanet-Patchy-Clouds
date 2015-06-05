#! /usr/bin/env python
from __future__ import print_function, division
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""comment
"""

if __name__ == '__main__':
    df125 = pd.read_csv('TinyTimF125Result.csv', parse_dates = {'datetime':['OBSDATE', 'OBSTIME']}, index_col = 'datetime')
    fig1 = plt.figure(1)
    ax1 = fig1.add_subplot(111)

    # for orbit in [1, 3, 5]:
    #     subdf = df125[df125['ORBIT'] == orbit]
    #     ax1.plot(subdf['DITHER']+1, subdf['FLUXA']/subdf['FLUXA'].mean(), 's', label = '{0}'.format(orbit), ms = 8)

    # ax1.set_xlabel('Dither')
    # ax1.set_xlim([0.5, 4.5])

    # fig2 = plt.figure(2)
    # ax2 = fig2.add_subplot(111)


    # for orbit in [2, 4, 6]:
    #     subdf = df125[df125['ORBIT'] == orbit]
    #     ax2.plot(subdf['DITHER']+1, subdf['FLUXA']/subdf['FLUXA'].mean(), 's', label = '{0}'.format(orbit), ms = 8)

    df125['flux0'] = np.zeros(len(df125))
    for angle in range(2):
        for dither in range(4):
            df125.loc[(df125['POSANGLE'] == angle) & (df125['DITHER'] == dither),'flux0'] = df125[(df125['POSANGLE'] == angle) & (df125['DITHER'] == dither)]['FLUXA']/df125[(df125['POSANGLE'] == angle) & (df125['DITHER'] == dither)]['FLUXA'].median()

    plt.plot(df125.index, df125['flux0'], 'o')
    plt.gca().set_ylim(0.98, 1.02)
    # ax2.set_xlabel('Dither')
    # ax2.set_xlim([0.5, 4.5])
    plt.show()
    
    
