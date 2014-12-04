#! /usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from astropy.io import fits
import os
import glob

        

def plotCR(fits_file):
    """
    find cosmic ray and plot it
    """
    sigma_list = [np.std(fits_file[ext].data) for ext in range(2, len(fits_file))] # calculate the standard deviation of each residual image
    sigma = np.min(sigma_list)
    ## the pixels that have value greater than 5 sigma will be treated as CR
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(np.arcsinh(fits_file[1].data), cmap = 'gray')
    symbol = ['|', '+', '^', 's', 'p']
    print len(fits_file)
    for ext in range(2, len(fits_file)):
        res_im = fits_file[ext].data
        crx, cry = np.where((res_im > 3 * sigma) | (res_im < - 3 * sigma))

        ax.plot(cry, crx, marker = symbol[ext - 2], ls = '', mew = 1.0, label = '{0}'.format(ext - 1))

    ax.legend(loc = 'lower right')
    ax.autoscale(tight = True)
    ax.set_xtitle = 'x'
    ax.set_ytitle = 'y'
    return fig

if __name__ == '__main__':
    target = 'ABPIC-B'
    aim_dir = os.path.join('.', target, 'CR_removed')
    #fits_fn = os.path.join('.', target, 'CR_removed', 'orbit_07_dither_01_F125W.fits')
    for fits_fn in glob.glob(os.path.join(aim_dir, '*.fits')):
        print fits_fn
        fits_content = fits.open(fits_fn)
        fig = plotCR(fits_content)
        ax = fig.axes[0]
        ax.set_title(fits_fn.split('/')[-1].split('.')[0])
        fig.savefig(fits_fn.replace(".fits", '.pdf'))
        fits_content.close()

        
    