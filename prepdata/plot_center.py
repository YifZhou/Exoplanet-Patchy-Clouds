#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from astropy.io import fits


def plotCircles(xcen, ycen, circleColor):
    """
    return a list of matplotlib pathces
    """
    circ = []
    circ.append(plt.Circle((xcen, ycen), 5, fc = 'none', ec = circleColor))
    circ.append(plt.Circle((xcen, ycen), 20, fc = 'none', ec = circleColor))
    circ.append(plt.Circle((xcen, ycen), 40, fc = 'none', ec = circleColor))
    return circ
    
if __name__ == '__main__':
    target = 'ABPIC-B'
    dataDir = os.path.join(os.pardir, 'data', target, 'CR_removed/')
    x_cen, y_cen = np.loadtxt('cntrd_result.dat', unpack = True)
    x_gcen, y_gcen = np.loadtxt('gcntrd_result.dat', unpack = True)
    x_corr, y_corr = np.loadtxt('crosscorr_result.dat', unpack = True)
    for i, fitsfn in enumerate(sorted(glob.glob(os.path.join(dataDir, '*.fits')))):
        fits_file = fits.open(fitsfn)
        im = fits_file[1].data
        fig, ax = plt.subplots()
        ax.imshow(np.arcsinh(fits_file[1].data), cmap = 'gray')
        ax.plot(x_cen[i], y_cen[i], 'rx', mew = 1.0, ms = 6)
        circ = plotCircles(x_cen[i], y_cen[i], 'r')
        for circle in circ:
            ax.add_patch(circle)
            
        ax.plot(x_gcen[i], y_gcen[i], 'bx', mew = 1.0, ms = 6)
        gcirc = plotCircles(x_gcen[i], y_gcen[i], 'b')
        for gcircle in gcirc:
            ax.add_patch(gcircle)

        ax.plot(x_corr[i], y_corr[i], 'gx', mew = 1.0, ms = 6)
        corr_circ = plotCircles(x_corr[i], y_corr[i], 'g')
        for circle in corr_circ:
            ax.add_patch(circle)
        

        ax.set_title(fitsfn.split('/')[-1].rstrip('.fits'))
        fig.savefig(fitsfn.replace('.fits', '.pdf').split('/')[-1])
        plt.close(fig)
        fits_file.close()
        