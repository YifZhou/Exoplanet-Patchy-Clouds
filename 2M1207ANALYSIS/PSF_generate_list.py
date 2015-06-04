#! /usr/bin/env python
from __future__ import print_function
import numpy as np
import os
import sys
from pyTinyTim import pyTinyTim
import pickle
#import sys
"""
Use Tinytim to generate a PSFs
"""


# xy = [[[135,161], [145,161], [135,173], [145,173]],
#       [[142, 159],[152,159], [142, 171], [152, 171]]]
def exposureFocus(MJD0):
    """
    the spline function is saved in a pickle file
    """
    focus0 = -0.24
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
    jitxList = np.arange(0,50,10)
    jityList = np.arange(0,50,10)
    xc = int(sys.argv[1])+380
    yc = int(sys.argv[2])+380
    filterName = sys.argv[3]
    MJD = float(sys.argv[4])
   
    aimDIR = os.path.join('.','PSF_temp')
    if not os.path.exists(aimDIR):
        os.mkdir(aimDIR)
    PSFFNFile = open( 'fn.dat', 'w')
    for jitx in jitxList:
        for jity in jityList:
            psfFN = pyTinyTim(xc, yc, filterName, jitx, jity, exposureFocus(MJD), outputDIR = aimDIR)
            PSFFNFile.write(os.path.join(aimDIR, psfFN) + '\n')

    PSFFNFile.close()