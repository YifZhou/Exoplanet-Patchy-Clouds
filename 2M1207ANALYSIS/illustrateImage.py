#! /usr/bin/env python
from __future__ import print_function, division
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm
plt.style.use('paper')
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
    ax1.plot(15.855, 8.204, 'o', ms=36, mfc='none', mew=2.5, mec='white')
    ax1.annotate('2M1207b', xy=(18.855, 8.204), xytext=(18.5, 7),
                 fontsize='18', color='white', weight='bold')
    ax1.set_title('F160W Image of 2M1207 A and b')
    ax1.set_xlim([0, 26])
    ax1.set_ylim([0, 26])
    sub = im - psf
    bd2 = np.concatenate((-np.logspace(-0.24, -1, 50) * 5,
                          np.linspace(-0.1, 0.1, 5),
                          np.logspace(-1, 1.3, 150) * 5))
    cax2 = ax2.imshow(sub, cmap='hot', origin='lower',
                      interpolation='nearest',
                      norm=BoundaryNorm(bd2, ncolors=255))
    ax2.set_title('Primary Subtraction Reveals 2M1207 b')
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

    PSF1 = fits.getdata('./fitsResult/PSF1.fits', 0)
    PSF2 = fits.getdata('./fitsResult/PSF2.fits', 0)
    fig3, ax3 = plt.subplots()
    cax3 = ax3.imshow(PSF1, cmap='hot', origin='lower',
                      interpolation='nearest',
                      norm=BoundaryNorm(bd1, ncolors=255))
    ax3.set_title('TinyTim PSF for 2M1207A')
    ax3.set_xlim([0, 26])
    ax3.set_ylim([0, 26])
    cbar3 = fig3.colorbar(cax3, ticks=np.logspace(-1, 4, 6))
    cbar3.formatter = mpl.ticker.LogFormatter()
    cbar3.update_ticks()
    ax3.set_xlabel('X (pixel)')
    ax3.set_ylabel('Y (pixel)')
    fig3.savefig('TT_2M1207A.pdf')

    fig4, ax4 = plt.subplots()
    cax4 = ax4.imshow(PSF2, cmap='hot', origin='lower',
                      interpolation='nearest',
                      norm=BoundaryNorm(np.logspace(-3, 2, 255), ncolors=255))
    ax4.set_title('TinyTim PSF for 2M1207b')
    ax4.set_xlim([0, 26])
    ax4.set_ylim([0, 26])
    cbar4 = fig4.colorbar(cax4, ticks=np.logspace(-3, 2, 6))
    cbar4.formatter = mpl.ticker.LogFormatter()
    cbar4.update_ticks()
    ax4.set_xlabel('X (pixel)')
    ax4.set_ylabel('Y (pixel)')
    fig4.savefig('TT_2M1207b.pdf')

    residual = fits.getdata('./fitsResult/residual.fits', 0)
    fig5, ax5 = plt.subplots()
    cax5 = ax5.imshow(residual, cmap='hot', origin='lower',
                      interpolation='nearest',
                      norm=BoundaryNorm(np.linspace(-30, 30, 255), ncolors=255))
    ax5.set_title('Correction map')
    ax5.set_xlim([0, 26])
    ax5.set_ylim([0, 26])
    cbar5 = fig5.colorbar(cax5, ticks=np.linspace(-30, 30, 6))
    # cbar5.formatter = mpl.ticker.LogFormatter()
    cbar5.update_ticks()
    ax5.set_xlabel('X (pixel)')
    ax5.set_ylabel('Y (pixel)')
    fig5.savefig('TT_residual.pdf')
