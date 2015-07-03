#! /usr/bin/env python
from __future__ import print_function, division
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""plot the correlation of binned data
bin within one orbit
"""


def normFlux(dataFrame, normDither=False):
    """    Keyword Arguments:
    dataFrame  -- input data frame
    normDither -- (default False) if normalize by dither position, default
    is faulse
    reurn the normalized flux for primary and secondary
    """
    fluxA0 = np.zeros(len(dataFrame))
    fluxB0 = np.zeros(len(dataFrame))
    if normDither:
        for angle in [0, 1]:
            for dither in range(4):
                subDF_id = np.where((dataFrame['POSANGLE'] == angle) &
                                    (dataFrame['DITHER'] == dither))
                subDF = dataFrame[(dataFrame['POSANGLE'] == angle) &
                                  (dataFrame['DITHER'] == dither)]
                fluxA0[subDF_id] = subDF['FLUXA'] / subDF['FLUXA'].mean()
                fluxB0[subDF_id] = subDF['FLUXB'] / subDF['FLUXB'].mean()
    if not normDither:
        fluxA0 = dataFrame['FLUXA'] / dataFrame['FLUXA'].mean()
        fluxB0 = dataFrame['FLUXB'] / dataFrame['FLUXB'].mean()

    return fluxA0, fluxB0

if __name__ == '__main__':
    fn125 = '2015_Jun_24TinyTimF125Result.csv'
    fn160 = '2015_Jun_24TinyTimF160Result.csv'
    df125 = pd.read_csv(
        fn125, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    df160 = pd.read_csv(
        fn160, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    f125A0, f125B0 = normFlux(df125, normDither=True)
    f160A0, f160B0 = normFlux(df160, normDither=True)
    F125A = []
    F125B = []
    for orbit in range(1, 7):
        F125A.append(f125A0[np.where(df125['ORBIT'] == orbit)].mean())
        F125B.append(f125B0[np.where(df125['ORBIT'] == orbit)].mean())
    F125A = np.array(F125A)
    F125B = np.array(F125B)
    plt.close('all')
    plt.plot(range(1, 7), F125A / max(F125A), 'o', label='A', ms=14)
    plt.plot(range(1, 7), F125B / max(F125B), 's', label='B', ms=14)
    plt.xlabel('ORBIT')
    plt.ylabel('Normed Flux')
    plt.xlim([0.5, 6.5])
    plt.ylim([0.95, 1.005])
    plt.title('F125W')
    plt.legend(loc='lower left')
    plt.savefig('binned_coor_F125W.pdf')
    plt.clf()
    F160A = []
    F160B = []
    for orbit in range(1, 7):
        F160A.append(f160A0[np.where(df160['ORBIT'] == orbit)].mean())
        F160B.append(f160B0[np.where(df160['ORBIT'] == orbit)].mean())
    F160A = np.array(F160A)
    F160B = np.array(F160B)
    plt.plot(range(1, 7), F160A / max(F160A), 'o', label='A', ms=14)
    plt.plot(range(1, 7), F160B / max(F160B), 's', label='B', ms=14)
    plt.xlabel('ORBIT')
    plt.ylabel('Normed Flux')
    plt.xlim([0.5, 6.5])
    plt.ylim([0.95, 1.005])
    plt.title('F160W')
    plt.legend(loc='lower left')
    plt.savefig('binned_coor_F160W.pdf')
