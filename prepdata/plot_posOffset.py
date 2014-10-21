#! /usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    x_cen, y_cen = np.loadtxt('cntrd_result.dat', unpack = True, usecols = (1,2))
    x_gcen, y_gcen = np.loadtxt('gcntrd_result.dat', unpack = True, usecols = (1,2))
    x_corr, y_corr = np.loadtxt('crosscorr_result.dat', unpack = True, usecols = (1,2))
    x_wcs, y_wcs = np.loadtxt('WCS_result.dat', unpack = True, usecols = (1,2))
    obs_num = np.array(range(len(x_cen)))
    plt.subplots_adjust(top = 1, bottom = 0, wspace = 0)
    fig_x, axes = plt.subplots(figsize = (6, 8), nrows = 3, sharex = True)
    for ax in axes:
        ax.axvline(color = 'r', linestyle = '--')
    xbins = np.linspace(-0.3, 0.3, 15)
    #ax_x.plot(obs_num, 0 * obs_num, label = 'centroid')
    axes[0].hist(x_gcen - x_cen, bins = xbins, label = 'gcentroid')
    axes[0].set_ylabel('Gcentroid')
    axes[1].hist(x_corr - x_cen, bins = xbins, label = 'crosscorr')
    axes[1].set_ylabel('Crosscorr')
    axes[2].hist(x_wcs - x_cen, bins = xbins, label = 'WCS')
    axes[2].set_ylabel('WCS')
    axes[2].set_xlabel('Offset$_x$ (pixels)')
    fig_x.savefig('x_off.pdf')

    fig_y, axes  = plt.subplots(figsize = (6, 8), nrows = 3, sharex = True)
    for ax in axes:
        ax.axvline(color = 'r', linestyle = '--')
    ybins = np.linspace(-0.5, 0.5, 15)
#    ax_y.plot(obs_num, 0*obs_num, label = 'centroid')
    axes[0].hist(y_gcen - y_cen, bins = xbins, label = 'gcentroid')
    axes[0].set_ylabel('Gcentroid')
    axes[1].hist(y_corr - y_cen, bins = xbins, label = 'crosscorr')
    axes[1].set_ylabel('Crosscorr')
    axes[2].hist(y_wcs - y_cen, bins = xbins, label = 'WCS')
    axes[2].set_ylabel('WCS')
    axes[2].set_xlabel('Offset$_y$ (pixels)')
    fig_y.savefig('y_off.pdf')