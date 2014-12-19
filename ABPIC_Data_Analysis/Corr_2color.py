#! /usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import leastsq, curve_fit


#######Data file name, editable########
F125WInfoFile = 'f125info.csv'
F160WInfoFile = 'f160info.csv'
F125WFluxFile = 'Flux125_Dec01.dat'
F160WFluxFile = 'Flux160_Dec01.dat'
figureName = 'Flux_correlation_Dec18.pdf'
#######################################

## linear fit
def fitfunc(x, m, b):
    return m * x + b


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

if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111)
    flux125corr = []
    flux160corr = []
    err125corr = []
    err160corr = []
    for orbit_i in range(7, 13):
        flux125corr.append(f125DF[f125DF['orbit'] == orbit_i]['flux'][0:6])
        err125corr.append(f125DF[f125DF['orbit'] == orbit_i]['error'][0:6])
        flux160corr.append(f160DF[f160DF['orbit'] == orbit_i]['flux'])
        err160corr.append(f160DF[f160DF['orbit'] == orbit_i]['error'])
        
    flux125corr = np.array(flux125corr).flatten()
    err125corr = np.array(err125corr).flatten()
    flux160corr = np.array(flux160corr).flatten()
    err160corr = np.array(err160corr).flatten()
    ax.errorbar(flux125corr, flux160corr, xerr = err125corr, yerr = err160corr, fmt = 'o', ms = 4, capthick = 1)
    p, pcov = curve_fit(fitfunc, flux125corr, flux160corr, p0 = [1, 0], sigma = err160corr)
    x0 = np.linspace(flux125corr.min(), flux125corr.max(), 10)
    ax.plot(x0, p[0] * x0 + p[1])
    ax.text(1.80e-16, 1.62e-16, r'$y = {0:.2f}x + {1:.2e}$'.format(p[0],p[1]))
    ax.set_xlabel(r'F125W flux ($erg\,cm^{-2}s^{-1}\AA^{-1}$)')
    ax.set_ylabel(r'F160W flux ($erg\,cm^{-2}s^{-1}\AA^{-1}$)')
    ax.set_title('flux correlation (aperture radius = 5 pixels)')
    fig.tight_layout()
    fig.savefig(figureName)
    print p, pcov