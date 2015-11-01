#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import lombscargle  # lomb scargle method
from plotLightCurve import normFlux
# from lmfit import Model
from scipy.optimize import leastsq
import matplotlib as mpl
plt.style.use('paper')
"""measure the period of light curve
"""


def binNorm(df):
    fA, fB = normFlux(df, normDither=True)
    df['f0'] = fB  # add one column
    tBin = []
    fBin = []
    for orbit in range(1, 7):
        subdf = df[df['ORBIT'] == orbit]
        ditherSet = set(subdf['DITHER'])
        for dither in ditherSet:
            fBin.append(subdf[subdf['DITHER'] == dither]['f0'].median())
            tBin.append(subdf[subdf['DITHER'] == dither]['Time'].mean())
    return tBin, fBin


def fitfunc(p, x):
    return p[0] * np.sin((2 * np.pi / p[1]) * x + p[2]) + 1.0


def errfunc(p, x, y):
    return y - fitfunc(p, x)


if __name__ == '__main__':
    fn125 = '2015_Jun_24TinyTimF125Result.csv'
    fn160 = '2015_Jun_24TinyTimF160Result.csv'
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
    df160['Time'] = np.float32(
        df160.index.values - df125.index.values[0]) / (60 * 60 * 1e9)
    # print((df125['Time'].values[1:] - df125['Time'].values[:-1]) * 60)
    # print((df160['Time'].values[1:] - df160['Time'].values[:-1]) * 60)
    f125A0, f125B0 = normFlux(df125, normDither=True)
    f160A0, f160B0 = normFlux(df160, normDither=True)
    # I quit, trying matlab ...
    np.savetxt('F125Result.dat', np.c_[df125['Time'].values, f125A0, f125B0])
    np.savetxt('F160Result.dat', np.c_[df160['Time'].values, f160A0, f160B0])
    """
    according to calculation made by matlab
    For F125B amp=0.0139   T=10.9765    dphi=0.5874    baseline=1.0001
    """
    plt.close('all')
    fig = plt.figure()
    gs = mpl.gridspec.GridSpec(3, 2)
    axOut = fig.add_subplot(gs[:, :])
    axOut.set_xlabel('Time - 2014-04-11 08:07:47 [h]', labelpad=30)
    axOut.set_ylabel('Normalized flux', labelpad=56)
    ax125B = fig.add_subplot(gs[0:2, 0])
    df125_1 = df125[(df125['DITHER'] == 0) | (df125['DITHER'] == 2)]
    df125_2 = df125[(df125['DITHER'] == 1) | (df125['DITHER'] == 3)]
    tBin_125_1, fBin_125_1 = binNorm(df125_1)
    tBin_125_2, fBin_125_2 = binNorm(df125_2)
    # ax125B.plot(tBin_125_1, fBin_125_1, 'o')
    # ax125B.plot(tBin_125_2, fBin_125_2, 's')
    ax125B.plot(np.concatenate([tBin_125_1, tBin_125_2]),
                np.concatenate([fBin_125_1, fBin_125_2]), 'o')
    t = np.linspace(df125['Time'].min(), df125['Time'].max(), 500)
    modelFlux = 0.0139 * np.sin(2 * np.pi / 10.9765 * t + 0.5874) + 1.0001
    line125, = ax125B.plot(t, modelFlux, linewidth=1.8)

    points125, = ax125B.plot(df125['Time'], f125B0, '+',
                             ms=8, mec='0.8', zorder=0)

    ax125B.set_title('F125W Light Curve')

    # split the data

    f125A0_2, f125B0_2 = normFlux(df125_2, normDither=True)

    ax125A = fig.add_subplot(gs[2, 0])
    ax125A.plot(df125['Time'], f125A0, 'o', color='0.8', zorder=0)
    """For F160B I used two type fit,
    1. free parameter fit
    amp=0.0088    T=9.2692   dphi=-0.1180    baseline=1.0002
    2. fixed parameter fit
    amp=0.0080    T=10.9765  dphi=0.2525    baseline=0.9997
    """
    ax160B = fig.add_subplot(gs[0:2, 1])

    df160_1 = df160[(df160['DITHER'] == 0) | (df160['DITHER'] == 2)]
    df160_2 = df160[(df160['DITHER'] == 1) | (df160['DITHER'] == 3)]
    tBin_160_1, fBin_160_1 = binNorm(df160_1)
    tBin_160_2, fBin_160_2 = binNorm(df160_2)
    # ax160B.plot(tBin_160_1, fBin_160_1, 'o')
    # ax160B.plot(tBin_160_2, fBin_160_2, 's')
    ax160B.plot(np.concatenate([tBin_160_1, tBin_160_2]),
                np.concatenate([fBin_160_1, fBin_160_2]), 'o')
    t = np.linspace(df160['Time'].min(), df160['Time'].max(), 500)
    modelFlux1 = 0.0080 * np.sin(2 * np.pi / 10.9765 * t + 0.2525) + 0.9997
    modelFlux2 = 0.0088 * np.sin(2 * np.pi / 9.2692 * t - 0.1180) + 1.0002
    # line160_1, = ax160B.plot(t, modelFlux1, label='P=10.9', linewidth=1.8)
    line160_2, = ax160B.plot(t, modelFlux2, label='P=9.3', linewidth=1.8)
    points160, = ax160B.plot(df160['Time'], f160B0, '+',
                             ms=8, mec='0.8', zorder=0)
    ax160B.set_title('F160W Light Curve')
    # ax160B.legend()
    ax160A = fig.add_subplot(gs[2, 1])
    ax160A.plot(df160['Time'], f160A0, 'o', color='0.8', zorder=0)

    # adjust the labels and gridspec
    for ax in [ax125B, ax160B, axOut]:
        # ax.get_xaxis().set_visible(False)
        ax.set_xticks([])
        ax.set_ylim([0.95, 1.05])
    for ax in [ax160A, ax160B, axOut]:
        #        ax.get_yaxis().set_visible(False)
        ax.set_yticks([])
    # for ax in [ax125A, ax125B]:
    #     ax.set_ylabel('Normalized flux')
    for ax in [ax125A, ax160A]:
        #        ax.set_xlabel('Time (h)')
        ax.set_ylim([0.975, 1.025])
    for ax in [ax125A, ax160A]:
        ax.text(0.05, 0.05, '2M1207 A',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes)

    ax125A.yaxis.set_ticks([0.98, 1.00, 1.02])
    for ax in [ax125B, ax160B]:
        ax.text(0.05, 0.05, '2M1207 b',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes)
    gs.update(hspace=0, wspace=0)
    ax125A.set_xticks(ax125A.get_xticks()[0:-1])
    for ax in fig.axes:
        if ax is not axOut:
            ax.axhline(1, color='k', lw=1.8, ls='--')

    fig.tight_layout()
    plt.show()
    plt.savefig('sineCurveFit_binCombined.pdf')
