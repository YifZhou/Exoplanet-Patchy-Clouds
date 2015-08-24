#! /usr/bin/env python
from __future__ import print_function, division
import pandas as pd
import numpy as np

from plotLightCurve import normFlux
"""uncertainty analysis for the photometry
"""

if __name__ == '__main__':
    fn125 = '2015_Aug_16TinyTimF125Result.csv'
    fn160 = '2015_Aug_16TinyTimF160Result.csv'
    df125 = pd.read_csv(
        fn125, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    df125 = df125.sort_index()
    # time in ns
    df125['Time'] = np.float32(
        df125.index.values - df125.index.values[0]) / (60 * 60 * 1e9)

    df160 = pd.read_csv(
        fn160, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    df160 = df160.sort_index()
    # time in ns
    df160['Time'] = np.float32(
        df160.index.values - df160.index.values[0]) / (60 * 60 * 1e9)

    df125['err0'] = df125['FLUXERRB'] / df125['FLUXB']
    df160['err0'] = df160['FLUXERRB'] / df160['FLUXB']
    f125A0, f125B0 = normFlux(df125, normDither=True)
    f160A0, f160B0 = normFlux(df160, normDither=True)
    chisq125 = (((f125B0 - 1.0) / 0.0134)**2).sum()
    chisq160 = (((f160B0 - 1.0) / 0.0112)**2).sum()
    print(chisq125 / (len(f125B0) - 1))
    print(chisq160 / (len(f160B0) - 1))
    model125 = 0.0139 * np.sin(2 * np.pi / 10.9765 * df125['Time'] + 0.5874)\
        + 1.0001
    model160 = 0.0088 * np.sin(2 * np.pi / 9.2692 * df160['Time'] - 0.1180)\
        + 1.0002
    chisq125_1 = (((f125B0 - model125) /
                   0.0134)**2).sum()
    chisq160_1 = (((f160B0 - model160) /
                   0.0112)**2).sum()
    print(chisq125_1 / (len(f125B0) - 3))
    print(chisq160_1 / (len(f160B0) - 3))
    df125['FLUXB'] = f125B0
    df160['FLUXB'] = f160B0
    outputColumns = ['Time', 'FLUXB', 'err0']
    df125[outputColumns].to_csv('F125_PhotErr.csv', index=False)
    df160[outputColumns].to_csv('F160_PhotErr.csv', index=False)
