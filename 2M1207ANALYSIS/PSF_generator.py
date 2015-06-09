#! /usr/bin/env python
import sys
import os
from pyTinyTim import pyTinyTim
import pickle
#import sys
"""
Use Tinytim to generate a PSFs
"""

def exposureFocus(MJD0):
    """
    the spline function is saved in a pickle file
    """
    focus0 = -0.24 # constant focus offset for wfc3
    #MJD, focus = np.loadtxt('focus.dat', usecols = (0, 5), unpack = True)
    #spline = splineFunc(MJD, focus)
    spline = pickle.load(open('focus_splineFunc.pkl', 'rb'))
    #pickle.dump(open('focus_splineFunc.pkl', 'wb'))
    # newMJD = np.linspace(min(MJD), max(MJD), 100*len(MJD))
    # newFocus = spline(newMJD)
    # plt.plot(MJD, focus, '+')
    # plt.plot(newMJD, newFocus)
    return focus0 + spline(MJD0)

if __name__ == '__main__':
    inFile = open('2mass_psf.in', 'r').readlines()
    xc = float(sys.argv[1])
    yc = float(sys.argv[2])
    filterName = sys.argv[3]
    jitx = float(sys.argv[4])
    jity = float(sys.argv[5])
    MJD = float(sys.argv[6])
    dis = exposureFocus(MJD)
    outfn = sys.argv[7]
    aimDIR = os.getcwd()
    xc = xc + 380
    yc = yc + 380
    if not os.path.exists(aimDIR):
        os.mkdir(aimDIR)
    psfDIR = pyTinyTim(xc, yc, filterName, jitx, jity, dis, outputDIR = aimDIR, outputRoot = outfn)