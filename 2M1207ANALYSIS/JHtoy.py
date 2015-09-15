#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt

"""a toy model to show the JH band difference
"""


def changeRatio(tauRatio, length):
    return np.exp(-(tauRatio - 1) * length)

if __name__ == '__main__':
    l = np.logspace(-1, 1, 20)
    r = changeRatio(0.1, l)
    plt.close('all')
    plt.plot(l, r, '-', lw=2)
    plt.gca().set_xscale('log')
    plt.xlabel('Cloud Depth')
    plt.ylabel('Amplitude$_{J}$/Amplitude$_{H}$')
    plt.gca().set_ylim([1, 3])
    plt.show()
    plt.savefig('JHratio_toyModel.pdf')
