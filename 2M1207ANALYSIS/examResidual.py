#! /usr/bin/env python
from __future__ import print_function, division
from astropy.io import fits
import numpy as np

"""examine the residual
"""


def makeAnnulus(center, radius):
    """obtain annulus index
"""
    x, y = center
    xx, yy = np.meshgrid(np.arange(27), np.arange(27))
    distance = np.sqrt((xx - x)**2 + (yy - y)**2)
    idx, idy = np.where(distance < radius)
    return idx, idy

if __name__ == '__main__':
    residualFile = './fitsResult/icdg01a1q.fits'
    im = fits.getdata(residualFile, 0)
    psf = fits.getdata(residualFile, 1)
    residual = im - psf
    id1 = makeAnnulus([13, 13], 5)
    print(residual[id1].sum())
