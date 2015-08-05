from __future__ import print_function, division
import pandas as pd
import numpy as np

if __name__ == '__main__':
    fn125 = '2015_Jun_24TinyTimF125Result.csv'
    fn160 = '2015_Jun_24TinyTimF160Result.csv'
    df125 = pd.read_csv(
        fn125, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    df125 = df125.sort_index()
    df160 = pd.read_csv(
        fn160, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    df160 = df160.sort_index()
    contrast125 = np.log10(df125['FLUXA'] / df125['FLUXB']) * 2.5
    contrast160 = np.log10(df160['FLUXA'] / df160['FLUXB']) * 2.5
    print('F125W contrast: {0:.2f}$\pm${1:.2f}'.
          format(contrast125.mean(), contrast125.std()))
    print('F160W contrast: {0:.2f}$\pm${1:.2f}'.
          format(contrast160.mean(), contrast160.std()))
