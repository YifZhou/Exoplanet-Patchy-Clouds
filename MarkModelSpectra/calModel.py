#! /usr/bin/env python
from __future__ import print_function, division
from readSpec import readSpec
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

"""calculate model J vs H ratio
"""


def calModel(cloudyFN, clearFN, Jprofile, Hprofile):
    wlCloudy, fCloudy = readSpec(cloudyFN)
    wlClear, fClear = readSpec(clearFN)

    # interpolating the data so that their wavelengths match
    dw = 0.0001  # wavelength inter
    w = np.linspace(0.8, 3, (3 - 0.8) / dw)
    funcJ = interp1d(Jprofile[:, 0] / 1e4, Jprofile[:, 1],
                     kind='linear', bounds_error=False, fill_value=0)
    Jtrans = funcJ(w)
    funcH = interp1d(Hprofile[:, 0] / 1e4, Hprofile[:, 1],
                     kind='linear', bounds_error=False, fill_value=0)
    Htrans = funcH(w)
    funcCloudy = interp1d(wlCloudy, fCloudy,
                          kind='linear', bounds_error=False, fill_value=0)
    fCloudy = funcCloudy(w)
    funcClear = interp1d(
        wlClear, fClear, kind='linear', bounds_error=False, fill_value=0)
    fClear = funcClear(w)
    JCloudy = (Jtrans * fCloudy * dw).sum()
    JClear = (Jtrans * fClear * dw).sum()
    HCloudy = (Htrans * fCloudy * dw).sum()
    HClear = (Htrans * fClear * dw).sum()
    # return JClear, JCloudy, HClear, HCloudy
    return ((JClear - JCloudy) / (JClear + JCloudy)) /\
        ((HClear - HCloudy) / (HClear + HCloudy))


if __name__ == '__main__':
    Jprofile = np.loadtxt('F125W_transmission.dat')
    Hprofile = np.loadtxt('F160W_transmission.dat')

    TList = [900, 950, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700]
    JHratioHg = np.zeros(len(TList))
    JHratioLg = np.zeros(len(TList))
    for i, T in enumerate(TList):
        cloudyFN = 't' + str(T) + 'g300f3.flx'
        clearFN = 't' + str(T) + 'g300f5.flx'
        JHratioLg[i] = calModel(cloudyFN, clearFN, Jprofile, Hprofile)
    for i, T in enumerate(TList):
        cloudyFN = 't' + str(T) + 'g3000f3.flx'
        clearFN = 't' + str(T) + 'g3000f5.flx'
        JHratioHg[i] = calModel(cloudyFN, clearFN, Jprofile, Hprofile)

    plt.close()
    plt.plot(TList, JHratioLg, 'o', ms=10, mfc='none', mew=1, label='Low g')
    plt.plot(TList, JHratioHg, 'o', ms=10, mfc='k', mew=1, label='High g')
    plt.legend()
    plt.gca().invert_xaxis()
    plt.xlabel('T (K)')
    plt.ylabel(r'$(\Delta F_J/F_J)/(\Delta F_H/F_H)$')
    plt.title('Model Amp_J/Amp_H')
    plt.savefig('/Users/ZhouYf/Desktop/Model_JHratio.png')

    plt.xlim([1750, 1150])
    plt.ylim([0, 10])
    plt.title('Model Amp_J/Amp_H zoomed L to L/T transition')
    plt.savefig('/Users/ZhouYf/Desktop/Model_JHratio_zoomed.png')
