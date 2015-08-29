#! /usr/bin/env python
from __future__ import print_function, division
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('paper')
"""plot J-H ratio
"""

if __name__ == '__main__':
    tgName, specType, specPos, JHratio, JH = np.genfromtxt(
        'JHratio.dat', delimiter=',', unpack=True, dtype=str
    )

    specPos = np.float32(specPos)
    JHratio = np.float32(JHratio)
    JH = np.float32(JH)
    JHDeltaMag = -2.5 * np.log10(JHratio)
    plt.close('all')
    plt.scatter(specPos, JHratio, s=160, c=JH, cmap='coolwarm')
    cbar = plt.colorbar()
    cbar.set_label('J-H (mag)')
    # plt.plot(specPos, JHDeltaMag, 's')
    # plt.plot(5, -0.49, 'o', mec='b', mfc='none', ms=10, mew=1.5)
#    plt.plot(JH, JHDeltaMag, 's')
    # plt.plot(1.9, -0.55, 'o')
    # plt.xlabel('J-H')

    plt.xticks([5, 10.5, 12, 16.5], ['L5', 'T0.5', 'T2', 'T6.5'])
    plt.xlabel('Spectral type')
    plt.ylabel('Amptude$_{\mathrm{J}}$/Amptude$_{\mathrm{H}}$')
    for i in range(len(specPos)):
        plt.text(
            specPos[i] + 0.1, JHratio[i] + 0.02, tgName[i], fontsize=12)
    # plt.text(5.2, -0.58, '2M1207b', color='b')
    plt.show()
    plt.savefig('JH.pdf')
