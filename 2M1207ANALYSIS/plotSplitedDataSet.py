#! /usr/bin/env python
from __future__ import print_function, division
from plotLightCurve import normFlux
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

"""split the sample by dithering position
"""


def normedSin(t, p):
    return p[0] * np.sin((2 * np.pi / p[1]) * t + p[2]) + 1

if __name__ == '__main__':
    fn125 = '2015_Jun_24TinyTimF125Result.csv'
    fn160 = '2015_Jun_24TinyTimF160Result.csv'
    ##
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
    # df160 = df160[df160['ORBIT'] > 1]  # remove the data from the first orbit

    df125_1 = df125[(df125['DITHER'] == 1) | (df125['DITHER'] == 3)]
    df125_2 = df125[(df125['DITHER'] == 0) | (df125['DITHER'] == 2)]
    f125A0, f125B0 = normFlux(df125, normDither=True)
    f125A0_1, f125B0_1 = normFlux(df125_1, normDither=True)
    f125A0_2, f125B0_2 = normFlux(df125_2, normDither=True)

    # make the plot
    plt.close('all')
    fig125 = plt.figure(figsize=(8, 10))
    t125 = np.linspace(df125['Time'].min(), df125['Time'].max(), 200)
    # for all data
    ax1 = fig125.add_subplot(411)
    ax1.plot(df125['Time'], f125B0, 's', label='whole set')
    ax1.plot(t125, normedSin(t125, [0.0139, 10.9821, 0.5869]))
    ax2 = fig125.add_subplot(412, sharex=ax1)
    df125 = df125[df125['ORBIT'] > 1]  # remove the data from the first orbit
    f125A0, f125B0 = normFlux(df125, normDither=True)
    ax2.plot(df125['Time'], f125B0, 's', label='no orbit 1')
    ax2.plot(t125, normedSin(t125, [0.0139, 12.03, 0.7069]))
    ax3 = fig125.add_subplot(413, sharex=ax1)
    ax3.plot(df125_1['Time'], f125B0_1, 's', label='1st half')
    ax3.plot(t125, normedSin(t125, [0.0155, 8.7654, -0.1467]))
    ax4 = fig125.add_subplot(414, sharex=ax1)
    ax4.plot(df125_2['Time'], f125B0_2, 's', label='2nd half')
    ax4.plot(t125, normedSin(t125, [0.0159, 16.9621, 1.5753]))
    for ax in fig125.axes:
        ax.legend()
        ax.set_ylim([0.97, 1.03])
        ax.set_ylabel('normed flux')
    ax4.set_xlabel('Time (hr)')
    fig125.tight_layout()

    df160_1 = df160[(df160['DITHER'] == 1) | (df160['DITHER'] == 3)]
    df160_2 = df160[(df160['DITHER'] == 0) | (df160['DITHER'] == 2)]
    f160A0, f160B0 = normFlux(df160, normDither=True)
    f160A0_1, f160B0_1 = normFlux(df160_1, normDither=True)
    f160A0_2, f160B0_2 = normFlux(df160_2, normDither=True)
    fig160 = plt.figure(figsize=(8, 10))
    t160 = np.linspace(df160['Time'].min(), df160['Time'].max(), 200)
    # for all data
    ax1 = fig160.add_subplot(411)
    ax1.plot(df160['Time'], f160B0, 's', label='whole set')
    ax1.plot(t160, normedSin(t160, [0.0088, 9.3029, -0.1083]))
    ax2 = fig160.add_subplot(412, sharex=ax1)
    df160 = df160[df160['ORBIT'] > 1]  # remove the data from the first orbit
    f160A0, f160B0 = normFlux(df160, normDither=True)
    ax2.plot(df160['Time'], f160B0, 's', label='no orbit 1')
    ax2.plot(t160, normedSin(t160, [0.0085, 9.6673, 0.0294]))
    ax3 = fig160.add_subplot(413, sharex=ax1)
    ax3.plot(df160_1['Time'], f160B0_1, 's', label='1st half')
    ax3.plot(t160, normedSin(t160, [0.0062, 9.8892, 0.2633]))
    ax4 = fig160.add_subplot(414, sharex=ax1)
    ax4.plot(df160_2['Time'], f160B0_2, 's', label='2nd half')
    ax4.plot(t160, normedSin(t160, [0.0108, 9.1665, -0.2410]))
    for ax in fig160.axes:
        ax.legend()
        ax.set_ylim([0.97, 1.03])
        ax.set_ylabel('normed flux')
    ax4.set_xlabel('Time (hr)')
    fig160.tight_layout()
    plt.show()
