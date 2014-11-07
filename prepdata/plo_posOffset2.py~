#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys

if __name__ == '__main__':
    xoff, yoff = np.loadtxt(sys.argv[1], unpack = True)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(xoff, bins = 10)
    ax.set_xlabel('Offset (pixels)')
    ax.set_ylabel('Number of meaurement')
    fig.savefig(sys.argv[1].strip('.dat') + '.pdf')
    