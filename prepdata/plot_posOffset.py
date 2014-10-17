#! /usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    x_cen, y_cen = np.loadtxt('cntrd_result.dat', unpack = True, usecols = (1,2))
    x_gcen, y_gcen = np.loadtxt('gcntrd_result.dat', unpack = True, usecols = (1,2))
    x_corr, y_corr = np.loadtxt('crosscorr_result.dat', unpack = True, usecols = (1,2))
    x_wcs, y_wcs = np.loadtxt('WCS_result.dat', unpack = True, usecols = (1,2))
    obs_num = np.array(range(len(x_cen)))
    fig_x, ax_x  = plt.subplots()
    ax_x.plot(obs_num, 0 * obs_num, label = 'centroid')
    ax_x.plot(obs_num, x_gcen - x_cen, label = 'gcentroid')
    ax_x.plot(obs_num, x_corr - x_cen, label = 'crosscorr')
    ax_x.plot(obs_num, x_wcs - x_cen, label = 'WCS')
    ax_x.legend(loc = 'best')
    ax_x.set_xlabel('Observation No.')
    ax_x.set_ylabel('$\mathsf{Offset}_x$ (pixels)')
    fig_x.savefig('x_off.pdf')

    fig_y, ax_y  = plt.subplots()
    ax_y.plot(obs_num, 0*obs_num, label = 'centroid')
    ax_y.plot(obs_num, y_gcen - y_cen, label = 'gcentroid')
    ax_y.plot(obs_num, y_corr - y_cen, label = 'crosscorr')
    ax_y.plot(obs_num, y_wcs - y_cen, label = 'WCS')
    ax_y.legend(loc = 'best')
    ax_y.set_xlabel('Observation No.')
    ax_y.set_ylabel('$\mathsf{Offset}_y$ (pixels)')
    fig_y.savefig('y_off.pdf')