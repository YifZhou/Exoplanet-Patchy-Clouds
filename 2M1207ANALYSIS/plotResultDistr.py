#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.style.use('paper')
"""plot the distribution for period and amplitude
"""

if __name__ == '__main__':
    plt.close('all')
    pDist125, ampDist125 = np.loadtxt('F125W_Distr.csv', delimiter=',',
                                      unpack=True)
    pDist160, ampDist160 = np.loadtxt('F160W_Distr.csv', delimiter=',',
                                      unpack=True)

    pBins = np.linspace(6, 20, 29)
    fig_p, ax_p = plt.subplots()

    countP125, binP125 = np.histogram(pDist125, bins=pBins)
    countP160, binP160 = np.histogram(pDist160, bins=pBins)
    ax_p.bar(
        binP125[:-1], countP125 / len(pDist125), pBins[1] - pBins[0],
        alpha=0.8, label='F125W')
    ax_p.bar(
        binP160[:-1], countP160 / len(pDist160), pBins[1] - pBins[0],
        label='F160W', alpha=0.8, fc='#e41a1c')
    ax_p.legend()
    ax_p.set_xlabel('Period (hour)')
    ax_p.set_ylabel('Probability')

    ampBins = np.linspace(0.003, 0.026, 24)
    fig_amp, ax_amp = plt.subplots()
    countAmp125, binAmp125 = np.histogram(ampDist125, bins=ampBins)
    countAmp160, binAmp160 = np.histogram(ampDist160, bins=ampBins)
    ax_amp.bar(
        binAmp125[:-1], countAmp125 / len(ampDist125), ampBins[1] - ampBins[0],
        alpha=0.8, label='F125W')
    ax_amp.bar(
        binAmp160[:-1], countAmp160 / len(ampDist160), ampBins[1] - ampBins[0],
        label='F160W', alpha=0.8, fc='#e41a1c')
    ax_amp.legend()
    ax_amp.set_xlim([0.003, 0.026])
    ax_amp.set_xlabel('Amplitude')
    ax_amp.set_ylabel('Probability')

    fig_p.savefig('periodDistr.png')
    fig_amp.savefig('amplitudeDistr.png')
