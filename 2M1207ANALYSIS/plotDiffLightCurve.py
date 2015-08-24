#! /usr/bin/env python
from __future__ import print_function, division
from plotLightCurve import normFlux
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if __name__ == '__main__':
    fn125_1 = '2015_Jun_24TinyTimF125Result.csv'  # original
    fn125_2 = '2015_Jul_14TinyTimF125Result.csv'  # AFEM
#    fn125_3 = '2015_Jul_16TinyTimF125Result.csv'

    df125_1 = pd.read_csv(
        fn125_1, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    df125_1 = df125_1.sort_index()
    # time in ns
    df125_1['Time'] = np.float32(
        df125_1.index.values - df125_1.index.values[0]) / (60 * 60 * 1e9)
    fA125_1, fB125_1 = normFlux(df125_1, normDither=True)

    df125_2 = pd.read_csv(
        fn125_2, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    df125_2 = df125_2.sort_index()
    # time in ns
    df125_2['Time'] = np.float32(
        df125_2.index.values - df125_2.index.values[0]) / (60 * 60 * 1e9)
    fA125_2, fB125_2 = normFlux(df125_2, normDither=True)

    df125_3 = pd.read_csv(
        fn125_3, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    df125_3 = df125_3.sort_index()
    # time in ns
    df125_3['Time'] = np.float32(
        df125_3.index.values - df125_3.index.values[0]) / (60 * 60 * 1e9)
    fA125_3, fB125_3 = normFlux(df125_3, normDither=True)

    fig = plt.figure(figsize=(8, 10))
    ax_1 = fig.add_subplot(411)
    ax_1.plot(df125_1['Time'], fB125_1, 's', label='original')
    ax_2 = fig.add_subplot(412, sharex=ax_1)
    ax_2.plot(df125_2['Time'], fB125_2, 's', label='AFEM')
    ax_3 = fig.add_subplot(413, sharex=ax_1)
    ax_3.plot(df125_2['Time'], fB125_3, 's', label='scaling residual')
    for ax in fig.axes:
        ax.set_ylim([0.95, 1.05])
        ax.set_ylabel('Normed flux')
    ax_4 = fig.add_subplot(414, sharex=ax_1)
    ax_4.plot(df125_1['Time'], fB125_2 - fB125_1, 's', label='2-1')
    ax_4.plot(df125_1['Time'], fB125_3 - fB125_1, 's', label='3-1')
    ax_4.set_ylabel('Diff')
    for ax in fig.axes:
        ax.legend()
    plt.show()
    # plt.savefig('Diff.pdf')
