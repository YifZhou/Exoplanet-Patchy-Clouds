#! /usr/bin/env python
from __future__ import print_function, division
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('paper')
from linearFit import linearFit
"""plot J-H ratio
"""


def chisq(y, mody, sigma):
    return np.sum((y - mody)**2 / sigma**2)


if __name__ == '__main__':
    tgName, specType, specPos, JHratio, JH, ampJ, ampH, err, textPos\
        = np.genfromtxt(
            'JHratio.dat', delimiter=',', unpack=True, dtype=str
        )

    specPos = np.float32(specPos)
    JHratio = np.float32(JHratio)
    JH = np.float32(JH)
    JHDeltaMag = -2.5 * np.log10(JHratio)
    ampJ = np.float32(ampJ)
    ampH = np.float32(ampH)
    err = np.float32(err)
    plt.close('all')
    fig, ax = plt.subplots()
    cax = ax.scatter(
        specPos, JHratio, s=np.sqrt(ampJ) * 500, c=JH, cmap='coolwarm')
    cbar = fig.colorbar(cax)
    ax.errorbar(specPos, JHratio, yerr=JHratio * err, color='0.4', ls='',
                elinewidth=2)
    cbar.set_label('J-H (mag)')
#     plt.plot(specPos, JHDeltaMag, 's')
#     plt.plot(5, -0.49, 'o', mec='b', mfc='none', ms=10, mew=1.5)
# #    plt.plot(JH, JHDeltaMag, 's')
#     plt.plot(1.9, -0.55, 'o')
#     plt.xlabel('J-H')

    ax.set_xticks([5, 10.5, 12, 16.5])
    ax.set_xticklabels(['L5', 'T0.5', 'T2', 'T6.5'])
    ax.set_xlabel('Spectral type')
    ax.set_ylabel('Amplitude$_{\mathrm{J}}$/Amplitude$_{\mathrm{H}}$')

    for i in range(len(specPos)):
        ax.text(
            textPos[i], JHratio[i] + 0.02, tgName[i], fontsize=12, zorder=10)

    # fig1, ax1 = plt.subplots()
    # ax1.plot(specPos, ampJ, '+', label='J', ms=12, mew=1.5)
    # ax1.plot(specPos, ampH, 'x', label='H', ms=12, mew=1.5)
    # ax1.legend()
    # ax1.set_xticks([5, 10.5, 12, 16.5])
    # ax1.set_xticklabels(['L5', 'T0.5', 'T2', 'T6.5'])
    # ax1.set_xlabel('Spectral type')
    # ax1.set_ylabel('Peak-Peak Amplitude')

    # plt.text(5.2, -0.58, '2M1207b', color='b')
    b, m, _, _, _ = linearFit(specPos, JHratio, err * JHratio)
    chisq1 = chisq(JHratio, m * specPos + b, err * JHratio) / 4
    chisq2 = chisq(
        JHratio, np.zeros(JHratio.shape) +
        JHratio.min() + 0.25, err * JHratio) / 4
    print(chisq1)
    print(chisq2)
    ax.plot(np.linspace(4.5, 17, 10),
            np.linspace(4.5, 17, 10) * m + b, ls='--', lw=2.0, color='0.2',
            zorder=0)
    ax.set_title('J and H variation amplitude ratios')
    plt.show()
    fig.savefig('JH.pdf')
    # fig1.savefig('AmpvsSpecType.pdf')
