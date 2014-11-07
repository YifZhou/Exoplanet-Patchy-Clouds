#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys

if __name__ == '__main__':
    xshift, yshift, dx, dy = np.loadtxt(sys.argv[1], unpack = True)
    plt.plot(xshift, dx, '.')
    plt.xlabel('x shift (pixels)')
    plt.ylabel('x offset (pixels)')
    plt.gca().set_xlim([-2,2])
    plt.savefig(sys.argv[1].strip('.dat') + '.pdf')
