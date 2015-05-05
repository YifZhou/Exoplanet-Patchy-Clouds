#! /usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy as np

def plotLightCurve(origDF, newDF, filtername):
    """
    plot the light curve
    """
    plt.close('all')
    fig = plt.figure()
    ax = plt.subplot2grid((3,1), (0,0), rowspan = 2)
#    origDF['FLUX0'] = origDF['FLUX']
    origDF['FLUX0'] = origDF['FLUX']/origDF['FLUX'].mean()
    origDF['ERR0'] = origDF['FLUXERR']/origDF['FLUX']
    origDF['Time'] = np.float32(origDF.index.values - origDF.index.values[0])/(60 * 60 * 1e9) #time in ns

#    newDF['FLUX0'] = newDF['FLUX']
    newDF['FLUX0'] = newDF['FLUX']/newDF['FLUX'].mean()
    newDF['ERR0'] = newDF['FLUXERR']/newDF['FLUX']
    newDF['Time'] = np.float32(newDF.index.values - newDF.index.values[0])/(60 * 60 * 1e9) #time in ns


    t = origDF['Time'] - origDF['Time'].values[0]
    ax.errorbar(t, origDF['FLUX0'] + 0.04, yerr = origDF['FLUX0'] * origDF['ERR0'], fmt = 's', label = 'Original Flat', mec = '0.2', mew = 0.5)
    ax.errorbar(t, newDF['FLUX0'], yerr = newDF['FLUX0'] * newDF['ERR0'], fmt = 'o', label = 'Blob Flat', mec = '0.2', mew = 0.5)
    ax.axhline(y = 1.0, linestyle = '--', color = '0.2', linewidth = 0.8)    
    ax.axhline(y = 1.04, linestyle = '--', color = '0.2', linewidth = 0.8)
    ax.legend(loc = 'best')
    
    ax.set_ylabel('Normalized Flux', fontsize = 18, fontweight = 'semibold')
    ax.set_xlabel('Time (h)', fontsize = 18, fontweight = 'semibold')

    ax_diff = plt.subplot2grid((3,1), (2,0), sharex = ax)
    diff = origDF['FLUX0'].values - newDF['FLUX0'].values
    ax_diff.plot(t, diff, marker = 'x', lw = 0 ,color = 'k', label = 'stddev = {0:.3f}%,\n max - min = {1:.3f}%'.format(diff.std()*100, (diff.max() - diff.min())*100))
    ax_diff.axhline(y = 0.0, linestyle = '--', color = '0.2', linewidth = 0.8)
    ax_diff.legend(loc = 'best')
    ax_diff.set_xlabel('Time (h)', fontsize = 18, fontweight = 'semibold')
    ax_diff.set_ylabel('Original - New', fontsize = 18, fontweight = 'semibold')

    fig.suptitle('{0} flat field compare'.format(filtername))
    fig.tight_layout()
    plt.savefig('compare_flat_{0}.pdf'.format(filtername))
    
if __name__ == '__main__':
    origFN = sys.argv[1]
    newFN = sys.argv[2]
    origDF = pd.read_csv(origFN, parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    newDF = pd.read_csv(newFN, parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    plotLightCurve(origDF[origDF['FILTER'] == 'F125W'], newDF[newDF['FILTER'] == 'F125W'], 'F125W')
    plotLightCurve(origDF[origDF['FILTER'] == 'F160W'], newDF[newDF['FILTER'] == 'F160W'], 'F160W')