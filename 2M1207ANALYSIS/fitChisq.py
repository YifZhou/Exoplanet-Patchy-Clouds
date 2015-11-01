#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
import pandas as pd
from plotLightCurve import normFlux
from linearFit import linearFit
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
"""calculate chisq for two fit
"""


def normedSin(t, p):
    return p[0] * np.sin((2 * np.pi / p[1]) * t + p[2]) + 1


def chisq0(y, ymod, sigma, DoF):
    """calcualte reduced chisq"""
    return np.sum((y - ymod)**2 / sigma**2) / DoF


def linearChisq(x, y, sigma):
    if type(sigma) is int or float:
        sigma = np.array([sigma] * len(x))
    b, m, sigb, sigm, chisq = linearFit(x, y, sigma)
    return chisq


def allChisq(y, ymod, x, sigma):
    chisq_1 = chisq0(y, ymod, sigma, len(y) - 4)
    chisq_2 = chisq0(y, np.array([1] * len(y)),
                     sigma, len(y) - 1)
    chisq_3 = linearChisq(x, y, sigma)
    return chisq_1, chisq_2, chisq_3


def plotDistDistr(y, ymod, x, sigma):
    diff1 = y - ymod
    b, m, _, _, _ = linearFit(x, y, np.array([sigma] * len(x)))
    ymod2 = m * x + b
    diff2 = y - ymod2
    diffbin = np.linspace(-3, 3, 15)
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(121)
    sinFunc = interp1d(x, ymod, kind='cubic')
    t = np.linspace(x.min(), x.max(), 100)
    lines1 = ax1.plot(t, sinFunc(t))
    lines2 = ax1.plot(x, ymod2)
    ax1.plot(x, y, '.', color='k')
    ax1.set_xlabel('Time (h)')
    ax1.set_ylabel('Normalized Flux')

    ax2 = fig.add_subplot(122)
    ax2.hist(diff1 / sigma, diffbin, label='sinusoidal', lw=2,
             fc=lines1[0].get_color(), ec=lines1[0].get_color(), alpha=0.8)
    ax2.hist(diff2 / sigma, diffbin, label='linear', lw=2,
             fc='None', ec=lines2[0].get_color(), hatch=r'\\')
    ax2.set_ylim(0, 15)
    ax2.legend()
    ax2.set_xlabel(r'(Obs. - Model)/$\sigma$')
    ax2.set_ylabel('Counts')
    return fig


def removePoints(inDF, nOutliers=2):
    """remove outliers from each orbit
       nOutliers: number of outliers to remove in each orbit
    """
    outDF = inDF[inDF['ORBIT'] > 1]
    keepList = []
    for orbit in range(1, 7):  # loop over 6 orbits
        subDF = outDF[outDF['ORBIT'] == orbit]
        # calculate the distance of flux to the mean
        dist = (subDF['Flux0'] - subDF['Flux0'].mean()).abs()
        dist.sort()
        keepList += dist.index[:-nOutliers]
    outDF = outDF.loc[keepList]
    return outDF


def readDF(fn125, fn160):

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
    df125['Flux0'] = f125B0
    df160['Flux0'] = f160B0
    return df125, df160


if __name__ == '__main__':
    fn125 = '2015_Jun_24TinyTimF125Result.csv'
    fn160 = '2015_Jun_24TinyTimF160Result.csv'
    df125, df160 = readDF(fn125, fn160)

    sigma125 = 0.0134
    sigma160 = 0.0112
    f125Model = 0.0139 * \
        np.sin(2 * np.pi / 10.9765 * df125['Time'] + 0.5874) + 1.0001
    f160Model = modelFlux2 = 0.0088 * \
        np.sin(2 * np.pi / 9.2692 * df160['Time'] - 0.1180) + 1.0002

    # chisq125_1, chisq125_2, chisq125_3 = allChisq(
    #     df125['Flux0'].values, f125Model, df125['Time'].values, sigma125)

    # print('F125W all data:')
    # print(chisq125_1)
    # print(chisq125_2)
    # print(chisq125_3)

    # chisq160_1, chisq160_2, chisq160_3 = allChisq(
    #     df160['Flux0'].values, f160Model, df160['Time'].values, sigma160)
    # print('F160W all data:')
    # print(chisq160_1)
    # print(chisq160_2)
    # print(chisq160_3)

    # OrbitGT1_125 = np.where(df125.ORBIT > 1)
    # OrbitGT1_160 = np.where(df160.ORBIT > 1)

    # chisq125_11, chisq125_21, chisq125_31 = allChisq(
    #     df125['Flux0'].values[OrbitGT1_125], f125Model.values[OrbitGT1_125],
    #     df125['Time'].values[OrbitGT1_125], sigma125)

    # print('F125W Orbit > 1:')
    # print(chisq125_11)
    # print(chisq125_21)
    # print(chisq125_31)

    # chisq160_11, chisq160_21, chisq160_31 = allChisq(
    #     df160['Flux0'].values[OrbitGT1_160], f160Model.values[OrbitGT1_160],
    #     df160['Time'].values[OrbitGT1_160], sigma160)

    # # make the plot
    # plt.close('all')
    # fig125 = plotDistDistr(
    #     f125B0[OrbitGT1_125], f125Model.values[OrbitGT1_125],
    #     df125['Time'].values[OrbitGT1_125], sigma125)
    # fig125.axes[0].legend(
    #     fig125.axes[0].lines[:2], [r'$\chi^2={0:.3f}$'.format(chisq125_11),
    #                                r'$\chi^2={0:.3f}$'.format(chisq125_31)]
    # )
    # fig160 = plotDistDistr(
    #     f160B0[OrbitGT1_160], f160Model.values[OrbitGT1_160],
    #     df160['Time'].values[OrbitGT1_160], sigma160)
    # fig160.axes[0].legend(
    #     fig160.axes[0].lines[:2], [r'$\chi^2={0:.3f}$'.format(chisq160_11),
    #                                r'$\chi^2={0:.3f}$'.format(chisq160_31)]
    # )
    # fig125.savefig('chisq_F125W.pdf')
    # fig160.savefig('chisq_F160W.pdf')
    # print('F160W Orbit > 1:')
    # print(chisq160_11)
    # print(chisq160_21)
    # print(chisq160_31)

    df125_filtered = removePoints(df125)
    df125_filtered[['Time', 'Flux0']].to_csv('F125_filtered_result.csv',
                                             index=False, header=False)
    df160_filtered = removePoints(df160)
    df160_filtered[['Time', 'Flux0']].to_csv('F160_filtered_result.csv',
                                             index=False, header=False)
    f125Model1 = normedSin(df125_filtered['Time'], [0.0139, 12.2540, 0.9038])
    f160Model1 = normedSin(df160_filtered['Time'], [0.0093, 9.7618, 0.0077])

    chisq125_filtered = allChisq(
        df125_filtered['Flux0'], f125Model1, df125_filtered['Time'], sigma125)
    chisq160_filtered = allChisq(
        df160_filtered['Flux0'], f160Model1, df160_filtered['Time'], sigma160)
    print(chisq125_filtered)
    print(chisq160_filtered)
