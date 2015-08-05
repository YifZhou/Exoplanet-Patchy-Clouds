#! /usr/bin/env python
from __future__ import print_function, division
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm

"""make an image to illustrate the 2M1207 system
especially the difficulty
"""

if __name__ == '__main__':
    plt.close('all')
    im = fits.getdata('./fitsResult/example.fits', 0)
    psf = fits.getdata('./fitsResult/example.fits', 1)
    fig1 = plt.figure(1)
    fig2 = plt.figure(2)
    ax1 = fig1.add_subplot(111)
    ax2 = fig2.add_subplot(111)
    bd1 = np.logspace(np.log10(im.min()), np.log10(im.max()), 255)
    cax1 = ax1.imshow(im, cmap='hot', origin='lower',
                      interpolation='nearest',
                      norm=BoundaryNorm(bd1, ncolors=255))
    ax1.plot(15.855, 8.204, 'o', ms=14, mfc='none', mew=1.5, mec='white')
    ax1.annotate('2M1207 B', xy=(15.855, 8.204), xytext=(17, 7),
                 fontsize=14)
    ax1.set_xlim([0, 26])
    ax1.set_ylim([0, 26])
    sub = im - psf
    bd2 = np.concatenate((-np.logspace(-0.24, -1, 50) * 5,
                          np.linspace(-0.1, 0.1, 5),
                          np.logspace(-1, 1.3, 150) * 5))
    cax2 = ax2.imshow(sub, cmap='hot', origin='lower',
                      interpolation='nearest',
                      norm=BoundaryNorm(bd2, ncolors=255))
    cbar1 = fig1.colorbar(cax1, ticks=np.logspace(-1, 4, 6))
    cbar1.formatter = mpl.ticker.LogFormatter()
    cbar1.update_ticks()
    cbar2 = fig2.colorbar(cax2, ticks=[-1, 0, 1, 10, 100])
    cbar2.formatter = mpl.ticker.LogFormatter()
    cbar2.update_ticks()

    for ax in [ax1, ax2]:
        ax.set_xlabel('X (pixel)')
        ax.set_ylabel('Y (pixel)')

    # plt.show()
    fig1.savefig('original.pdf')
    fig2.savefig('subtracted.pdf')
