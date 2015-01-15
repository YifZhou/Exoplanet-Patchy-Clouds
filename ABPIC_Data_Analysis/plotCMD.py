#! /usr/bin/env python
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import leastsq, curve_fit


#######Data file name, editable########
F125WInfoFile = 'f125info.csv'
F160WInfoFile = 'f160info.csv'
F125WFluxFile = 'Flux125_Dec01.dat'
F160WFluxFile = 'Flux160_Dec01.dat'
figureName = 'CMD_Jan09.pdf'
#######################################

f125DF = pd.read_csv(F125WInfoFile)
f160DF = pd.read_csv(F160WInfoFile)
f125flux, f125err = np.loadtxt(F125WFluxFile, unpack = True)
f160flux, f160err = np.loadtxt(F160WFluxFile, unpack = True)

photFlam125 = 2.2484e-20
photFlam160 = 1.9276e-20

f125DF['flux'] = f125flux * photFlam125
f125DF['error'] = f125err * photFlam125
f160DF['flux'] = f160flux * photFlam160
f160DF['error'] = f160err * photFlam160

def plx2dis(plx):
    """
    in Dupuy 2012, parallax in marcsec
    convert parallax to pc
    """
    return 1000/plx

def mag2Mag(mag, dis):
    """
    convert magnitude to absolute magnitude
    """
    return mag - 5 * (np.log10(dis) - 1)

def DeltaMag(flux, f0):
    """
    Calculate delta magnitude
    """
    return -2.5 * np.log10(flux/f0)

if __name__ == '__main__':
    MagTable = pd.read_csv('Dupuy2012_LT_Dwars_PhotTable.csv')
    MagTable[['J2mag', 'H2mag', 'plx']] = MagTable[['J2mag', 'H2mag', 'plx']].astype(float)
    MagTable['Distance'] = plx2dis(MagTable['plx'])
    MagTable['J20mag'] = mag2Mag(MagTable['J2mag'], MagTable['Distance'])
    MagTable['H20mag'] = mag2Mag(MagTable['H2mag'], MagTable['Distance'])
    J0 = MagTable[MagTable['Object'] == 'AB_Pic~b']['J20mag'].values
    H0 = MagTable[MagTable['Object'] == 'AB_Pic~b']['H20mag'].values
    flux125corr = []
    flux160corr = []
    err125corr = []
    err160corr = []
    for orbit_i in range(7, 13):
        flux125corr.append(f125DF[f125DF['orbit'] == orbit_i]['flux'].values[0:6])
        err125corr.append(f125DF[f125DF['orbit'] == orbit_i]['error'].values[0:6])
        flux160corr.append(f160DF[f160DF['orbit'] == orbit_i]['flux'].values)
        err160corr.append(f160DF[f160DF['orbit'] == orbit_i]['error'].values)

    flux125corr = np.array(flux125corr).flatten()
    print flux125corr/flux125corr.mean()
    err125corr = np.array(err125corr).flatten()
    flux160corr = np.array(flux160corr).flatten()
    err160corr = np.array(err160corr).flatten()
    JList = J0 + DeltaMag(flux125corr, flux125corr.mean())
    HList = H0 + DeltaMag(flux160corr, flux160corr.mean())
    fig = plt.figure(figsize = (6, 8))
    ax = fig.add_subplot(111)
    ax.plot(JList - HList, JList, '+', mew = 1.0)
    ax.plot(MagTable['J20mag'] - MagTable['H20mag'], MagTable['J20mag'], '.', mew = 0.8, color = '0.8', zorder = 0)
    #ax.set_ylim([12, 13])
    ax.invert_yaxis()
    ax.set_xlabel('Color (J-H)')
    ax.set_ylabel('Absolute J Magnitude')

    ax_abpic = fig.add_axes([0.2, 0.6, 0.32, 0.32])
    ax_abpic.plot(JList - HList, JList, '+', mew = 1.0)
    ## linear fit
    def fitfunc(x, m, b):
        return m * x + b
        
    p, pcov = curve_fit(fitfunc, JList-HList, JList, p0 = [-5, 0], sigma = 2.5 * err125corr/flux125corr)
    print p
    x = np.linspace((JList-HList).min(), (JList-HList).max(), 5)
    ax_abpic.plot(x, p[0] * x + p[1])
    ax.arrow((J0-H0)[0], J0[0], -0.2, -0.2*p[0])
    ax_abpic.set_aspect('equal')
    # ax_abpic.plot(MagTable['J20mag'] - MagTable['H20mag'], MagTable['J20mag'], '.', mew = 0.8, color = '0.8', zorder = 0)
    ax_abpic.set_xlim([1.46, 1.52])
    ax_abpic.set_ylim([12.84, 12.9])
    ax_abpic.xaxis.set_ticks([1.46, 1.48, 1.50, 1.52])
    ax_abpic.yaxis.set_ticks([12.84,12.86,12.88, 12.90])
    ax_abpic.invert_yaxis()
    fig.tight_layout()
    fig.savefig(figureName)