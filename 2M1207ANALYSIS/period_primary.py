#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import lombscargle  # lomb scargle method
from plotLightCurve import normFlux
#from lmfit import Model
from scipy.optimize import leastsq
"""measure the period of light curve
"""


# def sinFunc(x, amp, T, phi0):
#     return amp * np.sin((2 * np.pi / T) * x + phi0) + 1

def fitfunc(p, x):
    return p[0] * np.sin((2 * np.pi / p[1]) * x + p[2]) + 1.0


def errfunc(p, x, y):
    return y - fitfunc(p, x)


if __name__ == '__main__':
    fn125 = '2015_Jun_24TinyTimF125Result.csv'
    fn160 = '2015_Jun_24TinyTimF160Result.csv'
    df125 = pd.read_csv(
        fn125, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    df125 = df125.sort_index()
    # time in ns
    df125['Time'] = np.float32(
        df125.index.values - df125.index.values[0]) / (60 * 60 * 1e9)

    df160 = pd.read_csv(
        fn160, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    df160 = df160.sort_index()
    df160['Time'] = np.float32(
        df160.index.values - df160.index.values[0]) / (60 * 60 * 1e9)
    f125A0, f125B0 = normFlux(df125, normDither=True)
    f160A0, f160B0 = normFlux(df160, normDither=True)
    # I quit, trying matlab ...
    np.savetxt('F125Result.dat', np.c_[df125['Time'].values, f125A0, f125B0])
    np.savetxt('F160Result.dat', np.c_[df160['Time'].values, f160A0, f160B0])
    """
    according to calculation made by matlab
    For F125A amp=0.0139   T=10.9765    dphi=0.5874    baseline=1.0001
    """
    plt.close('all')
    fig = plt.figure()
    ax125 = fig.add_subplot(111)
    points125, = ax125.plot(df125['Time'], f125A0, 'o')
    t = np.linspace(df125['Time'].min(), df125['Time'].max(), 500)
    modelFlux = 0.0041 * np.sin(2 * np.pi / 6.8618 * t - 8.1991) + 1.0008
    line125, = ax125.plot(t, modelFlux)
    ax125.set_title('F125W')
    plt.savefig('sineCurveFit_primary.pdf')
    # """For F160B I used two type fit,
    # 1. free parameter fit
    # amp=0.0088    T=9.2692   dphi=-0.1180    baseline=1.0002
    # 2. fixed parameter fit
    # amp=0.0080    T=10.9765  dphi=0.2525    baseline=0.9997
    # """
    # ax160 = fig.add_subplot(212)
    # points160, = ax160.plot(df160['Time'], f160B0, 'o')
    # t = np.linspace(df160['Time'].min(), df160['Time'].max(), 500)
    # modelFlux1 = 0.0080 * np.sin(2 * np.pi / 10.9765 * t + 0.2525) + 0.9997
    # modelFlux2 = 0.0088 * np.sin(2 * np.pi / 9.2692 * t - 0.1180) + 1.0002
    # ax160.set_title('F160W')
    # for ax in [ax125, ax160]:
    #     ax.set_xlabel('Time (h)')
    #     ax.set_ylabel('Nomalized Flux')
    #     ax.legend()
    # fig.tight_layout()
    # plt.savefig('sineCurveFit.pdf')
