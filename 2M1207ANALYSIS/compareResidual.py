#! /usr/bin/env python
from __future__ import print_function, division

"""make a movie to show the residual pattern
"""
from astropy.io import fits
import pandas as pd
import numpy as np
from scipy.ndimage.interpolation import shift
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
plt.switch_backend('Qt4Agg')


class UpdateDist(object):

    def __init__(self, ax, df):
        self.success = 0
        self.axImage = ax.matshow(np.zeros((27, 27)),
                                  cmap='hot', vmin=-20, vmax=20)
        self.title = ax.set_title('')
        self.ax = ax

        # Set up plot parameters
        self.ax.set_xlim([0, 27])
        self.ax.set_ylim([0, 27])
        # sort by angle and dither position
        self.dataFrame = df.sort(['POSANGLE', 'DITHER'])

    def init(self):
        self.success = 0
        self.axImage.set_data(np.zeros((27, 27)))
        self.title.set_text('')
        return self.axImage, self.title

    def getPSF(self, iFile):
        """obtain PSF from saved fits file
        and shift them so that for different dither position,
        images align
        """
        # central pixel coordinate for different dither position
        xy0 = [[[135, 161], [145, 161], [135, 173], [145, 173]],
               [[142, 159], [152, 159], [142, 171], [152, 171]]]
        dataPath = './fitsResult/'
        fn = self.dataFrame['FILENAME'].values[iFile]
        angle = self.dataFrame['POSANGLE'].values[iFile]
        dither = self.dataFrame['DITHER'].values[iFile]
        # obtain central pixel coord for specific exposure
        x, y = xy0[int(angle)][int(dither)]
        # calculate the difference of PSF center relative to the image center
        dx = self.dataFrame['PRIMARY_X'].values[iFile] - x
        dy = self.dataFrame['PRIMARY_Y'].values[iFile] - y
        fn = fn.rstrip('_flt.fits') + '.fits'
        im = fits.getdata(dataPath + fn, 0)
        psf = fits.getdata(dataPath + fn, 1)
        return shift(im - psf, [-dy, -dx])

    def __call__(self, i):
        # This way the plot can continuously run and we just keep
        # watching new realizations of the process
        if i == 0:
            return self.init()
        angle = self.dataFrame['POSANGLE'].values[i]
        dither = self.dataFrame['DITHER'].values[i]
        self.axImage.set_array(self.getPSF(i))
        self.title.set_text('Angle = {0}, Dither = {1}'.format(
            angle + 1, dither + 1))
        return self.axImage, self.title

if __name__ == '__main__':
    plt.close('all')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    df = pd.read_csv('2015_Jun_17TinyTimF125Result.csv', parse_dates={
                     'datetime': ['OBSDATE', 'OBSTIME']},
                     index_col='datetime')
    ud = UpdateDist(ax, df)
    anim = FuncAnimation(fig, ud, frames=np.arange(len(df)), init_func=ud.init,
                         interval=200, blit=False)
    plt.show()
