#! /usr/bin/env python
import numpy as np
import os
from pyTinyTim import pyTinyTim
#import sys
"""
Use Tinytim to generate a PSFs
"""


xy = [[[135,161], [145,161], [135,173], [145,173]],
      [[142, 159],[152,159], [142, 171], [152, 171]]]

if __name__ == '__main__':
    inFile = open('2mass_psf.in', 'r').readlines()
    xc, yc = 515, 541
    jitxList = np.arange(0,50,10)
    jityList = np.arange(0,50,10)
    disList = np.arange(0, 2.0, 0.2) #fix displacement at 3.0
    for angle in [0, 1]:
        for dither in range(4):
            for jitx in jitxList:
                for jity in jityList:
                    for dis in disList:
                        aimDIR = os.path.join('.','PSF', 'angle_{0}_dither_{1}'.format(angle, dither))
                        #aimDIR = os.path.join(os.getcwd(), 'PSFs')
                        if not os.path.exists(aimDIR):
                            os.mkdir(aimDIR)
                        psfDIR = pyTinyTim(xc, yc, 'F125W', jitx, jity, dis, outputDIR = aimDIR)