#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import splev, splrep
# using spline to fit for the histogram, and find the period
"""calculate the  range of the period fitting result
"""


def PeriodRange(pDensity, bins):
    tck = splrep(bins, pDensity)
    return tck


if __name__ == '__main__':
    pDist125, ampDist125 = np.loadtxt('F125W_Distr.csv', delimiter=',',
                                      unpack=True, usecols=(0, 1))
    pDist160, ampDist160 = np.loadtxt('F160W_Distr.csv', delimiter=',',
                                      unpack=True, usecols=(0, 1))
    pDist = np.loadtxt('fixP_fitResult.csv', delimiter=',',
                       unpack=True, usecols=(0,))
    pBins = np.linspace(6, 20, 200)
    midBins = (pBins[:-1] + pBins[1:]) / 2
    dBin = pBins[1] - pBins[0]
    countP125, binP125 = np.histogram(pDist125, bins=pBins, normed=1)
    countP160, binP160 = np.histogram(pDist160, bins=pBins, normed=1)
    countP, binP = np.histogram(pDist, bins=pBins, normed=1)
    # fig, ax = plt.subplots()
    # bars125 = ax.bar(
    #     midBins, countP125, dBin,
    #     alpha=0.8, label='F125W', fc='#377eb8')
    # finerBins = np.linspace(6, 20, 500)
    # interpFunc = PeriodRange(countP125, midBins)
    # ax.plot(finerBins, splev(finerBins, interpFunc))
    # plt.show()
    cumCountP125 = countP125.cumsum() / countP125.sum()
    cumCountP160 = countP160.cumsum() / countP160.sum()
    cumCountP = countP.cumsum() / countP.sum()
    p125 = midBins[countP125 == countP125.max()][0]
    p160 = midBins[countP160 == countP160.max()][0]
    p = midBins[countP == countP.max()][0]
    p125_floor = midBins[
        cumCountP125 <= cumCountP125[midBins == p125] - 0.32][-1]
    p125_ceil = midBins[
        cumCountP125 >= cumCountP125[midBins == p125] + 0.32][0]

    p160_floor = midBins[
        cumCountP160 <= cumCountP160[midBins == p160] - 0.32][-1]
    p160_ceil = midBins[
        cumCountP160 >= cumCountP160[midBins == p160] + 0.32][0]

    p_floor = midBins[
        cumCountP <= cumCountP[midBins == p] - 0.32][-1]
    p_ceil = midBins[
        cumCountP >= cumCountP[midBins == p] + 0.32][0]
    print(p125, p125_floor, p125_ceil)
    print(p160, p160_floor, p160_ceil)
    print(p, p_floor, p_ceil)
    plt.close('all')
    plt.plot(midBins, cumCountP125)
    plt.plot(midBins, cumCountP160)
    plt.plot(midBins, cumCountP)
    plt.show()
