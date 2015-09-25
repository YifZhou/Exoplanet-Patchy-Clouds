#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
import matplotlib as plt


"""read Mark Marley's model spectra
"""


def readSpec(fn):
    wl, f = np.loadtxt(fn, unpack=True, usecols=(1, 3))
    return wl, f

if __name__ == '__main__':
    wl, f = readSpec('t1000g1000f5.flx')
    plt.plot(wl, f, '.')
    plt.show()
