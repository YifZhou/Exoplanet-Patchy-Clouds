#! /usr/bin/env python
from __future__ import print_function, division
from astropy.io import fits
from astropy import wcs
from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
"""plot the astrometry measrurement
"""

markers = ['_', '+', '^', 's', 'p', 'h']
colors = mpl.rcParams['axes.color_cycle']


def getRADec(df, dataPath='../data/2M1207B/'):
    """do the plot
    """
    RA_a = np.zeros(len(df))
    Dec_a = np.zeros(len(df))
    RA_b = np.zeros(len(df))
    Dec_b = np.zeros(len(df))
    for i, index in enumerate(df.index):
        header = fits.getheader(dataPath + df['FILENAME'][index], 1)
        WCS = wcs.WCS(header)
        RA_i, Dec_i = WCS.wcs_pix2world(
            df['PRIMARY_X'][index], df['PRIMARY_Y'][index], 1)
        RA_a[i] = RA_i
        Dec_a[i] = Dec_i
        RA_i, Dec_i = WCS.wcs_pix2world(
            df['SECONDARY_X'][index], df['SECONDARY_Y'][index], 1)
        RA_b[i] = RA_i
        Dec_b[i] = Dec_i
    return SkyCoord(RA_a * u.deg, Dec_a * u.deg, frame='icrs'),\
        SkyCoord(RA_b * u.deg, Dec_b * u.deg, frame='icrs')


def plotDitherAstrometry(df):
    """the function to do this
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212, sharex=ax1)
    for angle in [0, 1]:
        for dither in range(4):
            pos = angle * 4 + dither
            subdf = df[(df['POSANGLE'] == angle) & (df['DITHER'] == dither)]
            for orbit in range(6):
                ax1.plot([pos] * len(subdf[subdf['ORBIT'] == orbit + 1]),
                         subdf[subdf['ORBIT'] == orbit + 1]['Pos Angle'],
                         linewidth=0, marker=markers[orbit],
                         ms=8, mew=2, mec=colors[orbit],
                         color=colors[orbit], alpha=0.8)
                ax2.plot([pos] * len(subdf[subdf['ORBIT'] == orbit + 1]),
                         subdf[subdf['ORBIT'] == orbit + 1]['Separation'],
                         linewidth=0, marker=markers[orbit],
                         ms=8, mew=2, mec=colors[orbit],
                         color=colors[orbit], alpha=0.8)

            ax1.errorbar(pos + 0.1, subdf['Pos Angle'].mean(),
                         yerr=subdf['Pos Angle'].std(),
                         fmt='o', color='k', elinewidth=2.5, zorder=5)
            ax2.errorbar(pos + 0.1, subdf['Separation'].mean(),
                         yerr=subdf['Separation'].std(),
                         fmt='o', color='k', elinewidth=2.5, zorder=5)

    ax1.set_xlabel('Position')
    ax1.set_ylabel('Pos Angle (deg)')
    ax2.set_xlabel('Posintion')
    ax2.set_ylabel('Separation (arcsec)')
    return fig

if __name__ == '__main__':
    plt.close('all')
    df125 = pd.read_csv('2015_Jun_24TinyTimF125Result.csv', parse_dates={
        'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    primary_pos, secondary_pos = getRADec(df125)
    df125['Pos Angle'] = np.array(
        primary_pos.position_angle(secondary_pos).to(u.deg))
    df125['Separation'] = np.array(
        primary_pos.separation(secondary_pos).to(u.arcsec))
    fig1 = plotDitherAstrometry(df125)
    fig1.suptitle('F125W')

    df160 = pd.read_csv('2015_Jun_24TinyTimF160Result.csv', parse_dates={
        'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    primary_pos, secondary_pos = getRADec(df160)
    df160['Pos Angle'] = np.array(
        primary_pos.position_angle(secondary_pos).to(u.deg))
    df160['Separation'] = np.array(
        primary_pos.separation(secondary_pos).to(u.arcsec))
    fig2 = plotDitherAstrometry(df160)
    fig2.suptitle('F160W')

    for fig in [fig1, fig2]:
        fig.tight_layout()
    plt.show()
