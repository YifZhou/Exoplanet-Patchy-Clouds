from __future__ import print_function, division
import pandas as pd
import numpy as np
from plotLightCurve import normFlux

if __name__ == '__main__':
    fn125 = '2015_Jun_24TinyTimF125Result.csv'
    fn160 = '2015_Jun_24TinyTimF160Result.csv'
    df125 = pd.read_csv(
        fn125, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    df125 = df125.sort_index()
    df125['Time'] = np.float32(
        df125.index.values - df125.index.values[0]) / (60 * 60 * 1e9)
    df160 = pd.read_csv(
        fn160, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    df160 = df160.sort_index()
    df160['Time'] = np.float32(
        df160.index.values - df160.index.values[0]) / (60 * 60 * 1e9)
    contrast125 = np.log10(df125['FLUXA'] / df125['FLUXB']) * 2.5
    contrast160 = np.log10(df160['FLUXA'] / df160['FLUXB']) * 2.5
    print('F125W contrast: {0:.2f}$\pm${1:.2f}'.
          format(contrast125.mean(), contrast125.std()))
    print('F160W contrast: {0:.2f}$\pm${1:.2f}'.
          format(contrast160.mean(), contrast160.std()))

    # standard deviation of one measurement
    model125 = 0.0139 * np.sin(2 * np.pi / 10.9765 * df125['Time'] + 0.5874)\
        + 1.0001
    model160 = 0.0088 * np.sin(2 * np.pi / 9.2692 * df160['Time'] - 0.1180)\
        + 1.0002
    f125A0, f125B0 = normFlux(df125, normDither=True)
    f160A0, f160B0 = normFlux(df160, normDither=True)
    std125 = (f125B0 - model125).std()
    std160 = (f160B0 - model160).std()

    print('F125W stddev: {0:.2f}%'.format(std125 * 100))
    print('F160W stddev: {0:.2f}%'.format(std160 * 100))
