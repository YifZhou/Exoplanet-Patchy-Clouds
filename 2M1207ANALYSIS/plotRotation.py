#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
"""plot the rotation rate vs mass
"""

if __name__ == '__main__':
    name, mass, radius, period, label = np.genfromtxt(
        'rotationRate.dat', delimiter=',', dtype=str, skip_header=1,
        unpack=True
    )
    mass = np.float32(mass)  # in Mjup
    radius = np.float32(radius)  # in R_jup
    period = np.float32(period)  # in hours
    v_equ = 2 * np.pi * (radius * 69911) / (period * 3600)  # in km/s
    plt.close('all')
    fig_p, ax_p = plt.subplots()
    ax_p.set_xscale('log')
    # ax_p.set_yscale('log')

    ax_p.plot(mass[0], period[0], 's', ms=10)
    ax_p.plot(mass[1:], period[1:], 's', ms=10)
    ax_p.errorbar(
        [0.00017, 0.00256], [25, 25], yerr=2, lolims=True, color='k', ls='')
    ax_p.set_ylim(0, 30)
    # ax.arrow(x0, y0, 0, -0.3, fc='b', lw=0.2, head_width=0.05,
    # head_length=0.1)

    ax_p.set_xlabel('M (M$_{\mathrm{Jup}}$)')
    ax_p.set_ylabel('Period (hour)')
    BDperiod = np.array([2.7, 1.55, 2.7, 3.8, 4.1, 3.2, 13,
                         2.5, 11, 3.9, 2.6, 4.2, 18, 19, 3.5, 1.41])
    ax_p.plot(np.zeros(len(BDperiod)) + 30, BDperiod,
              'o', mec='k', mfc='none', ms=10)
    ax_p.add_patch(patches.Rectangle((15, BDperiod.mean() - BDperiod.std()),
                                     35, 2 * BDperiod.std(),
                                     fc='0.8', alpha=0.8))

    for i in range(len(name)):
        if i == 4:
            ax_p.text(mass[i] * 1.3, period[i] - 1.5, label[i])
        elif i == 5:
            ax_p.text(mass[i] * 1.3, period[i], label[i])
        elif i == 6:
            ax_p.text(mass[i] / 5.5, period[i] - 0.5, label[i])
        else:
            ax_p.text(mass[i] * 1.3, period[i] - 0.5, label[i])
    ax_p.text(0.00017, 28, 'Mercury')
    ax_p.text(0.00256, 28, 'Venus')
    plt.show()
    plt.savefig('rotationDiagram.pdf')
    # fig_v, ax_v = plt.subplots()
    # ax_v.plot(np.log10(mass), np.log10(v_equ), 's')
    # ax_v.set_xlabel('$\log(M/M_{\mathrm{Jup}})$')
    # ax_v.set_ylabel('$\log(v/(\mathrm{km\cdot s^{-1}}))$')
    # for i in range(len(name)):
    #     if i < 7:
    #         ax_v.text(np.log10(mass[i]) + 0.1, np.log10(v_equ[i]) + 0.05,
    #                   label[i])
    #     else:
    #         ax_v.text(np.log10(mass[i]) + 0.1, np.log10(v_equ[i]) - 0.25,
    #                   label[i])
    # plt.show()
