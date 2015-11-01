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
    # ax_p.plot(mass[0], v_equ[0], 's', ms=10)
    # ax_p.plot(mass[1:], v_equ[1:], 's', ms=10)
    ax_p.errorbar(
        [0.00017, 0.00256], [26, 26], yerr=2.0,
        lolims=True, color='k', ls='')
    ax_p.errorbar(4, 10.05, xerr=[1], yerr=[[0.9], [0.8]], color='k')

    # ax.arrow(x0, y0, 0, -0.3, fc='b', lw=0.2, head_width=0.05,
    # head_length=0.1)

    ax_p.set_xlabel('M (M$_{\mathrm{Jup}}$)')
    ax_p.set_ylabel('Period (hour)')
    # ax_p.set_ylabel('Equatorial rotation velocity (km$\cdot$s$^{-1}$)')
    BDperiod = np.array([2.7, 1.55, 2.7, 3.8, 4.1, 3.2, 13,
                         2.5, 11, 3.9, 2.6, 4.2, 18, 19, 3.5, 1.41])
    vBD = 2 * np.pi * (1 * 69911) / (BDperiod * 3600)
    # suppose BD has period of 1 Mjup
    ax_p.plot(np.zeros(len(BDperiod)) + 30, BDperiod,
              'o', mec='k', mfc='none', ms=10, label='Metchev et al. (2015)')
    ax_p.text(45, 10, 'Brown dwarfs', rotation=90)
    # ax_p.plot(np.zeros(len(BDperiod)) + 30, vBD,
    #           'o', mec='k', mfc='none', ms=10)
    ax_p.add_patch(patches.Rectangle((15, BDperiod.mean() - BDperiod.std()),
                                     35, 2 * BDperiod.std(),
                                     fc='0.8', alpha=0.8))
    # ax_p.add_patch(patches.Rectangle((15, vBD.mean() - vBD.std()),
    #                                  35, 2 * vBD.std(),
    #                                  fc='0.8', alpha=0.8))

    for i in range(len(name)):
        if i == 4:
            ax_p.text(mass[i] / 2.0, period[i] + 1.2, label[i], fontsize=16)
        elif i == 5:
            ax_p.text(mass[i] / 2.0, period[i] - 1.5, label[i], fontsize=16)
        elif i == 6:
            ax_p.text(mass[i] / 6.5, period[i], label[i], fontsize=16)
        elif i == 0:
            ax_p.text(mass[i] / 1.5, period[i] + 1.2, label[i], fontsize=16)
        else:
            ax_p.text(mass[i] * 1.3, period[i], label[i], fontsize=16)
    ax_p.text(0.00017 * 1.2, 26, 'Mercury', fontsize=16)
    ax_p.text(0.00256 * 1.2, 26, 'Venus', fontsize=16)

    Pperiod = np.array([21.4, 4.08, 2.91, 19.35, 9.64, 25.81,
                        18.46, 20.16, 40.27])
    Pmass = np.array([250., 80, 100, 150, 130, 250, 180, 130, 150])
    # ax_p.plot(Pmass, Pperiod, 's', mfc='none', label='Pleiades')

    Omass = np.array([0.17, 0.05, 0.08, 0.22, 0.27, 0.21, 0.27,
                      0.06, 0.12, 0.09, 0.16, 0.12, 0.12, 0.18,
                      0.04, 0.02, 0.12, 0.02, 0.22, 0.19, 0.18,
                      0.14, 0.05, 0.11, 0.06, 0.19, 0.29, 0.05,
                      0.04, 0.11]) * 1000  # convert to jupiter mass
    Operiod = np.array([56.1, 9.46, 35.2, 100.0, 18.0, 96.8,
                        100.4, 19.2, 31.0, 14.6, 15.7, 33.7,
                        102.1, 40.1, 15.5, 4.70, 3.80, 5.79,
                        45.1, 30.0, 38.5, 11.4, 87.6, 35.9,
                        16.9, 98.0, 82.5, 34.3, 4.06, 32.3])
    # ax_p.plot(Omass, Operiod, '^', mfc='none', label='$\epsilon$ Ori')
    # ax_p.legend()
    ax_p.set_ylim(0, 30)
    # ax_p.set_xlim(1e-4, 5e2)
    ax_p.set_title('Rotation Periods of planets and Brown Dwarfs')
    ax_p.plot(4, 5, 's', ms=12, mfc='red', alpha=0.4)
    ax_p.arrow(4, 9, 0, -2.2, fc='0.4', ec='0.4', lw=3,
               head_width=1.2, head_length=0.8)
    ax_p.plot(7, 3.0, 's', ms=12, mfc='blue', alpha=0.4)
    ax_p.arrow(7, 7.2, 0, -2.4, fc='0.4', ec='0.4', lw=3,
               head_width=1.8, head_length=0.8)
    ax_p.set_ylim(0, 29)

    BDperiod2 = np.loadtxt('scholz2015.dat')
    BDperiod2 = BDperiod2 * 24  # convert day to hour
    ax_p.plot(np.zeros(BDperiod2.shape) + 45, BDperiod2,
              '^', mec='b', mfc='none', ms=10, label='Scholz et al. (2015)')
    ax_p.legend(loc='best')
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
