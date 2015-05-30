#! /usr/bin/env python
from __future__ import print_function
import numpy as np
import os
from pyTinyTim import pyTinyTim

#import sys
"""
Use Tinytim to generate a PSFs
"""


xy = [[[95,208], [105,208], [95,219], [105,219]],
      [[129, 222],[139,222], [129, 233], [139, 233]]]

if __name__ == '__main__':
    inFile = open('abpic.in', 'r').readlines()
    jitxList = np.arange(0,50,10)
    jityList = np.arange(0,50,10)
    disList = np.arange(0, 3.6, 0.2) #fix displacement at 3.0
    if not os.path.exists('./PSF'):
        os.mkdir('./PSF')

    
    for angle in [0, 1]:
        for dither in range(4):
            for filter_name in ['F125W', 'F160W']:
                aimDIR = os.path.join('.','PSF', 'filter_{0}_angle_{1}_dither_{2}'.format(filter_name,angle, dither))
                if not os.path.exists(aimDIR):
                    os.mkdir(aimDIR)
                PSFFNFile = open(os.path.join('.','PSF', 'filter_{0}_angle_{1}_dither_{2}'.format(filter_name, angle, dither), 'fn.dat'), 'w')
                for jitx in jitxList:
                    for jity in jityList:
                        for dis in disList:                        
                            #aimDIR = os.path.join(os.getcwd(), 'PSFs')
                            xc, yc = xy[angle][dither]
                            xc = xc + 380
                            yc = yc + 380
                  
                            psfFN = pyTinyTim(xc, yc, filter_name, jitx, jity, dis, outputDIR = aimDIR)
                            PSFFNFile.write(psfFN + '\n')

                PSFFNFile.close()