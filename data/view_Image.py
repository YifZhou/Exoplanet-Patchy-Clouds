#! /usr/bin/env python
"""
use pyds9 to view image
"""
import ds9
import sys
import os
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def viewImage(fits_name):
    """
    function to open fits file and view then image
    """
    d = ds9.ds9()
    fits_content = fits.open(fits_name)
    target = fits_content[0].header['targname']
    if target == 'ABPIC-B':
        planet_coord = '06:19:12.94 -58:03:20.9' # RA and Dec of the planet in FK5 coordinate, data obtained from simbed, for pan the iamge to centered on the target
    elif target == '2M1207B':
        planet_coord = '12:07:33.467 -39:32:54.00'
    else:
        print 'target missing'
        return 1

        
    d.set(' '.join(['file', fits_name]))
    d.set('align yes')
    d.set('contour clear')
    d.set('cmap Cool')
    d.set(' '.join(['pan to', planet_coord, 'wcs fk5']))
    center = [float(num) for num in d.get('pan image').split()]
    d.set('scale histequ')
    d.set('scale mode 99.5')
    d.set('zoom 4')
    return center

def plotSurf(fits_name, center, radius = 30):
    fits_content = fits.open(fits_name)
    image = fits_content[1].data
    subimage = image[center - radius:center+radius][center-radius:center+radius]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.plot_surface(subimage)

if __name__ == '__main__':
    maindir = os.path.dirname(__file__)
    try:
        center = viewImage(os.path.join(maindir,sys.argv[1]))
        print center
    except IOError:
        print 'File does not exist!'
