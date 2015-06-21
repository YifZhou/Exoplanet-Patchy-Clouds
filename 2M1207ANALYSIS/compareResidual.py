#! /usr/bin/env python
from __future__ import print_function, division

"""show the residual pattern
"""
from astropy.io import fits
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
plt.switch_backend('Qt4Agg')


class UpdateDist(object):

    def __init__(self, ax, df):
        self.success = 0
        self.axImage = ax.matshow(np.zeros((27, 27)),
                                  cmap='hot', vmin=-10, vmax=50)
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

    def readPSF(self, fn):
        dataPath = './fitsResult/'
        fn = fn.rstrip('_flt.fits') + '.fits'
        im = fits.getdata(dataPath + fn, 0)
        psf = fits.getdata(dataPath + fn, 1)
        return im - psf

    def __call__(self, i):
        # This way the plot can continuously run and we just keep
        # watching new realizations of the process
        if i == 0:
            return self.init()

        # Choose success based on exceed a threshold with a uniform pick
        fn = self.dataFrame['FILENAME'].values[i]
        angle = self.dataFrame['POSANGLE'][i]
        dither = self.dataFrame['DITHER'][i]
        self.axImage.set_array(self.readPSF(fn))
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
    anim = FuncAnimation(fig, ud, frames=np.arange(100), init_func=ud.init,
                         interval=100, blit=False)
    plt.show()


# def readPSF(fn):
#     im = fits.getdata(fn, 0)
#     psf = fits.getdata(fn, 1)
#     return (im - psf)


# def makeMovie(df):
#     dataPath = './fitsResult/'
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     i = 0
#     for angle in [0, 1]:
#         for dither in range(4):
#             subdf = df[(df['POSANGLE'] == angle) & (df['DITHER'] == dither)]
#             for fn in subdf['FILENAME'].values:
#                 cax = ax.imshow(
#                     readPSF(dataPath + 'i' +
#                             fn.strip('_flt.fits') + '.fits'),
#                     interpolation='nearest', cmap='hot',
#                     vmin=-10, vmax=50)
#                 ax.set_title('Angle = {0}, Dither = {1}'.format(
#                     angle + 1, dither + 1))
#                 fig.colorbar(cax)
#                 fig.savefig('./temp/{0:0>3d}.png'.format(i))
#                 i += 1


# if __name__ == '__main__':
#     plt.close('all')

#     df = pd.read_csv('2015_Jun_17TinyTimF125Result.csv', parse_dates={
#                      'datetime': ['OBSDATE', 'OBSTIME']},
#                      index_col='datetime')
#     makeMovie(df)
