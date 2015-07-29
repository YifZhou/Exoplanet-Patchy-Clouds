#! /usr/bin/env python
import sys
import os
from pyTinyTim import pyTinyTim
#import sys
"""
Use Tinytim to generate a PSFs
"""

if __name__ == '__main__':
    inFile = open('2mass_psf.in', 'r').readlines()
    xc = float(sys.argv[1])
    yc = float(sys.argv[2])
    filterName = sys.argv[3]
    jitx = float(sys.argv[4])
    jity = float(sys.argv[5])
    dis = float(sys.argv[6])
    aimDIR = os.getcwd()
    xc = xc + 380
    yc = yc + 380
    if not os.path.exists(aimDIR):
        os.mkdir(aimDIR)
    psfDIR = pyTinyTim(xc, yc, filterName, jitx, jity, dis, outputDIR=aimDIR)
