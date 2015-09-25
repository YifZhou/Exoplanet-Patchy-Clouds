#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt


"""read Mark Marley's model spectra
"""


def readSpec(fn):
    wl, f = np.loadtxt(fn, unpack=True, usecols=(1, 3))
    return wl[np.where((wl > 0.8) & (wl < 3.0))],\
        f[np.where((wl > 0.8) & (wl < 3.0))]


if __name__ == '__main__':
    wl, f = readSpec('t1000g1000f5.flx')
    plt.plot(wl, f)
    # xplt.xlim([1, 3])
    plt.show()
