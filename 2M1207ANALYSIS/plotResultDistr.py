#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.style.use('paper')
from scipy.optimize import curve_fit
"""plot the distribution for period and amplitude
"""


def gauss(x, a, x0, sigma):
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2))

if __name__ == '__main__':
    plt.close('all')
    pDist125, ampDist125, phaseDist125 = np.loadtxt(
        'F125W_Distr.csv', delimiter=',', unpack=True)
    pDist160, ampDist160, phaseDist160 = np.loadtxt(
        'F160W_Distr.csv', delimiter=',', unpack=True)

    # pDist, ampDist125, ampDist160 = np.loadtxt('fixP_fitResult.csv',
    #                                            delimiter=',', unpack=True)
    # pBins = np.linspace(6, 20, 57)
    # fig_p, ax_p = plt.subplots()

    # # countP125, binP125 = np.histogram(pDist125, bins=pBins, normed=1)
    # # countP160, binP160 = np.histogram(pDist160, bins=pBins, normed=1)
    # countP, binP = np.histogram(pDist, bins=pBins, normed=1)
    # ax_p.bar(
    #     (pBins[:-1] + pBins[1:]) / 2, countP, pBins[1] - pBins[0],
    #     alpha=0.8, fc='#e41a1c')
    # # ax_p.bar(
    # #     binP160[:-1], countP160, pBins[1] - pBins[0],
    # #     label='F160W', alpha=0.8, fc='#377eb8')
    # # ax_p.legend()
    # ax_p.set_xlabel('Period (hour)')
    # ax_p.set_ylabel('Probability density (hour$^{-1}$)')

    ampBins = np.linspace(0.00, 0.025, 51)
    fineAmpBins = np.linspace(0.00, 0.025, 510)
    fig_amp, ax_amp = plt.subplots()
    countAmp125, binAmp125 = np.histogram(ampDist125, bins=ampBins, normed=1)
    countAmp160, binAmp160 = np.histogram(ampDist160, bins=ampBins, normed=1)
    gpAmp125, cov125 = curve_fit(gauss, (binAmp125[1:] + binAmp125[:-1]) / 2,
                                 countAmp125, p0=[100, 0.014, 0.005])
    gpAmp160, cov160 = curve_fit(gauss, (binAmp160[1:] + binAmp160[:-1]) / 2,
                                 countAmp160, p0=[150, 0.008, 0.005])
    bars125 = ax_amp.bar(
        binAmp125[:-1], countAmp125, ampBins[1] - ampBins[0],
        alpha=0.8, label='F125W', fc='#377eb8')
    ax_amp.plot(fineAmpBins, gauss(fineAmpBins, *gpAmp125),
                color=bars125[0].get_facecolor(), lw=2)
    bars160 = ax_amp.bar(
        binAmp160[:-1], countAmp160, ampBins[1] - ampBins[0],
        label='F160W', alpha=0.8, fc='#e41a1c')
    ax_amp.plot(fineAmpBins, gauss(fineAmpBins, *gpAmp160),
                color=bars160[0].get_facecolor(), lw=2)

    ax_amp.legend()
    ax_amp.set_xlim([0.003, 0.026])
    ax_amp.set_xlabel('Amplitude')
    ax_amp.set_ylabel('Probability density')
    print(gpAmp125)
    print(gpAmp160)
    # fig_p.savefig('periodDistr.pdf')
    # fig_amp.savefig('amplitudeDistr.pdf')
    plt.show()
