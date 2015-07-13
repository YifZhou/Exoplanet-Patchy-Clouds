#! /usr/bin/env python
from __future__ import print_function, division
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits

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
    cax1 = ax1.imshow(np.arcsinh(im), cmap='hot', origin='lower',
                      interpolation='nearest', vmin=0)
    ax1.plot(15.855, 8.204, '*', ms=14, mfc='white', mew=0.8)
    ax1.annotate('2M1207 B', xy=(15.855, 8.204), xytext=(17, 7),
                 fontsize=14)
    ax1.set_xlim([0, 26])
    ax1.set_ylim([0, 26])
    cax2 = ax2.imshow(np.arcsinh(im - psf), cmap='hot', origin='lower',
                      interpolation='nearest', vmin=0)
    # cbar1 = fig1.colorbar(cax1)
    # cbar2 = fig2.colorbar(cax2)
    for ax in [ax1, ax2]:
        ax.set_xlabel('X (pixel)')
        ax.set_ylabel('Y (pixel)')

    # plt.show()
    fig1.savefig('original.pdf')
    fig2.savefig('subtracted.pdf')
