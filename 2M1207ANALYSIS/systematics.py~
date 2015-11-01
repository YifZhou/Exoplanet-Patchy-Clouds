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


def normedSin(t, p):
    return p[0] * np.sin((2 * np.pi / p[1]) * t + p[2]) + 1


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
        df160.index.values - df160.index.values[0]) / (60 * 60 * 1e9)
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
    fig = plt.figure(figsize=(12, 9))

    gs = mpl.gridspec.GridSpec(3, 2)
    axOut = fig.add_subplot(gs[:, :])
    axOut.set_xlabel('Time (h)', labelpad=24)
    axOut.set_ylabel('Normalized flux', labelpad=42)
    ax125B = fig.add_subplot(gs[0, 0])
    df125_1 = df125[(df125['DITHER'] == 0) | (df125['DITHER'] == 2)]
    df125_2 = df125[(df125['DITHER'] == 1) | (df125['DITHER'] == 3)]
    tBin_125_1, fBin_125_1 = binNorm(df125_1)
    tBin_125_2, fBin_125_2 = binNorm(df125_2)
    ax125B.plot(tBin_125_1, fBin_125_1, 'o')
    ax125B.plot(tBin_125_2, fBin_125_2, 's')
    # ax125B.plot(np.concatenate([tBin_125_1, tBin_125_2]),
    #             np.concatenate([fBin_125_1, fBin_125_2]), 'o')
    t = np.linspace(df125['Time'].min(), df125['Time'].max(), 500)
    modelFlux = 0.0139 * np.sin(2 * np.pi / 10.9765 * t + 0.5874) + 1.0001
    line125, = ax125B.plot(t, modelFlux, linewidth=1.8)

    points125, = ax125B.plot(df125['Time'], f125B0, '+',
                             ms=8, mec='0.8', zorder=0)

    # ax125B.set_title('Validation Test: F125W')
    # remove the data from the first orbit
    df125 = df125[df125['ORBIT'] > 1]
    f125A0, f125B0 = normFlux(df125, normDither=True)
    f160A0, f160B0 = normFlux(df160, normDither=True)
    tBin_125_no1, fBin_125_no1 = binNorm(df125)
    t125 = np.linspace(df125['Time'].min(), df125['Time'].max(), 500)
    ax125_no1 = fig.add_subplot(gs[1, 0])
    f125A0, f125B0 = normFlux(df125, normDither=True)
    ax125_no1.plot(tBin_125_no1, fBin_125_no1, 'o')
    ax125_no1.plot(df125['Time'], f125B0, '+',
                   ms=8, mec='0.8', zorder=0, label='no orbit 1')

    ax125_no1.plot(t, normedSin(t, [0.0139, 12.03, 0.7069]), lw=1.8)
#    lg = ax125_no1.legend()
#    lg.draw_frame(False)

    fn125_AFEM = '2015_Jul_14TinyTimF125Result.csv'  # apply AFEM
    df125_AFEM = pd.read_csv(
        fn125_AFEM, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    df125_AFEM = df125_AFEM.sort_index()
    # time in ns
    df125_AFEM['Time'] = np.float32(
        df125_AFEM.index.values - df125_AFEM.index.values[0]) / (60 * 60 * 1e9)
    ax125_AFEM = fig.add_subplot(gs[2, 0])
    tBin_125_AFEM, fBin_125_AFEM = binNorm(df125_AFEM)
    t125_AFEM = np.linspace(df125_AFEM['Time'].min(),
                            df125_AFEM['Time'].max(), 500)

    f125A0_AFEM, f125B0_AFEM = normFlux(df125_AFEM, normDither=True)
    ax125_AFEM.plot(tBin_125_AFEM, fBin_125_AFEM, 'o')
    ax125_AFEM.plot(df125_AFEM['Time'], f125B0_AFEM, '+',
                    ms=8, mec='0.8', zorder=0, label="AFEM")

    ax125_AFEM.plot(t, normedSin(t, [0.0139, 10.97, 0.59]), lw=1.8)
    # lg = ax125_AFEM.legend()
    # lg.draw_frame(False)

    """For F160B I used two type fit,
    1. free parameter fit
    amp=0.0088    T=9.2692   dphi=-0.1180    baseline=1.0002
    2. fixed parameter fit
    amp=0.0080    T=10.9765  dphi=0.2525    baseline=0.9997
    """
    ax160B = fig.add_subplot(gs[0, 1])

    df160_1 = df160[(df160['DITHER'] == 0) | (df160['DITHER'] == 2)]
    df160_2 = df160[(df160['DITHER'] == 1) | (df160['DITHER'] == 3)]
    tBin_160_1, fBin_160_1 = binNorm(df160_1)
    tBin_160_2, fBin_160_2 = binNorm(df160_2)
    ax160B.plot(tBin_160_1, fBin_160_1, 'o')
    ax160B.plot(tBin_160_2, fBin_160_2, 's')
    # ax160B.plot(np.concatenate([tBin_160_1, tBin_160_2]),
    #             np.concatenate([fBin_160_1, fBin_160_2]), 'o')
    t = np.linspace(df160['Time'].min(), df160['Time'].max(), 500)
    modelFlux1 = 0.0080 * np.sin(2 * np.pi / 10.9765 * t + 0.2525) + 0.9997
    modelFlux2 = 0.0088 * np.sin(2 * np.pi / 9.2692 * t - 0.1180) + 1.0002
    line160_1, = ax160B.plot(t, modelFlux1, label='P=10.45 h', linewidth=1.8)
    line160_2, = ax160B.plot(t, modelFlux2, label='P=9.0 h', linewidth=1.8)
    points160, = ax160B.plot(df160['Time'], f160B0, '+',
                             ms=8, mec='0.8', zorder=0)
    # ax160B.set_title('Validation Test: F160W')
    ax160B.legend()

    df160 = df160[df160['ORBIT'] > 1]
    tBin_160_no1, fBin_160_no1 = binNorm(df160)
    t160 = np.linspace(df160['Time'].min(), df160['Time'].max(), 500)
    ax160_no1 = fig.add_subplot(gs[1, 1])
    f160A0, f160B0 = normFlux(df160, normDither=True)
    ax160_no1.plot(tBin_160_no1, fBin_160_no1, 'o')
    ax160_no1.plot(df160['Time'], f160B0, '+',
                   ms=8, mec='0.8', zorder=0, label='no orbit 1')

    ax160_no1.plot(t, normedSin(t, [0.0085, 9.6673, 0.0294]))
    # lg = ax160_no1.legend()
    # lg.draw_frame(False)

    fn160_AFEM = '2015_Jul_14TinyTimF160Result.csv'  # apply AFEM
    df160_AFEM = pd.read_csv(
        fn160_AFEM, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    df160_AFEM = df160_AFEM.sort_index()
    # time in ns
    df160_AFEM['Time'] = np.float32(
        df160_AFEM.index.values - df160_AFEM.index.values[0]) / (60 * 60 * 1e9)
    ax160_AFEM = fig.add_subplot(gs[2, 1])
    tBin_160_AFEM, fBin_160_AFEM = binNorm(df160_AFEM)
    t160_AFEM = np.linspace(df160_AFEM['Time'].min(),
                            df160_AFEM['Time'].max(), 500)
    f160A0_AFEM, f160B0_AFEM = normFlux(df160_AFEM, normDither=True)
    ax160_AFEM.plot(tBin_160_AFEM, fBin_160_AFEM, 'o')
    ax160_AFEM.plot(df160_AFEM['Time'], f160B0_AFEM, '+',
                    ms=8, mec='0.8', zorder=0, label="AFEM")

    ax160_AFEM.plot(t, normedSin(t, [0.0088, 9.27, -0.12]), lw=1.8)
    # lg = ax160_AFEM.legend()
    # lg.draw_frame(False)
    # ax160A = fig.add_subplot(gs[2, 1], sharex=ax160B)
    # ax160A.plot(df160['Time'], f160A0, 'o', color='0.8', zorder=0)
    # gs.update(hspace=0, wspace=0)
    # ax125A.set_xticks(ax125A.get_xticks()[0:-1])
    gs.update(hspace=0, wspace=0)
    ax125_AFEM.set_xticks(ax125_AFEM.get_xticks()[0:-1])
    for ax in [ax160B, ax160_no1, ax160_AFEM, axOut]:
        ax.set_yticklabels([])
    for ax in [ax125B, ax160B, ax125_no1, ax160_no1, axOut]:
        ax.set_xticklabels([])
    # for ax in [ax125B, ax125_no1, ax125_AFEM]:
    #     ax.set_ylabel('Normalized flux')
    for ax in fig.axes:
        ax.set_xlim([0, 9])
        ax.set_ylim([0.95, 1.05])
    # for ax in[ax125_AFEM, ax160_AFEM]:
    #     ax.set_xlabel('Time (h)')
    # ax125B.set_ylabel('Normalized flux')

    for ax in [ax125B, ax125_no1, ax125_AFEM]:
        ax.text(0.02, 0.05, 'F125W', transform=ax.transAxes,
                weight='bold', color='b')
    for ax in [ax160B, ax160_no1, ax160_AFEM]:
        ax.text(0.02, 0.05, 'F160W', transform=ax.transAxes,
                weight='bold', color='r')
    for ax in [ax125B]:
        ax.text(0.02, 0.90, 'Sinusoidal fit/Dither Position 1,3 vs. 2,4',
                weight='bold', transform=ax.transAxes)
    for ax in [ax125_no1]:
        ax.text(0.02, 0.90, 'Only Orbits 2-6',
                weight='bold', transform=ax.transAxes)
    for ax in [ax125_AFEM]:
        ax.text(0.02, 0.90, 'Effect of flat field uncertainties',
                weight='bold', transform=ax.transAxes)
    fig.suptitle('Verification Tests of the Photometric Modulations')
    fig.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()
    plt.savefig('systematics.pdf')
    # chisq125 = (((f125B0 - 1.0) / 0.015)**2).sum()
    # print(chisq125)
