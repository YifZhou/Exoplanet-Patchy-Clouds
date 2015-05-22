#! /usr/bin/env python
import subprocess as sp
import numpy as np
import os
#import sys
"""
Use Tinytim to generate a PSFs
"""


xy = [[[135,161], [145,161], [135,173], [145,173]],
      [[142, 159],[152,159], [142, 171], [152, 171]]]

def modifyIn(inFile, angle, dither, jitx, jity, secDis):
    xc, yc = xy[angle][dither]
    inFile[1] = 'Jitx_{0:0>2d}_Jity_{1:0>2d}_Dis_{2:0>2.2f}_angle_{3:d}_dither_{4:d}\n'.format(jitx, jity, secDis,angle, dither)
    inFile[9] = '{0:.5f} # Major axis jitter in mas\n'.format(jitx)
    inFile[10] = '{0:.5f} # Major axis jitter in mas\n'.format(jity)
    inFile[14] = '{0:d} {1:d}  # Position 1'.format(xc, yc)
    inFile[251] = '{0:.5f} #z4 = Focus\n'.format(secDis/100.)
    return inFile

if __name__ == '__main__':

    inFile = open('2mass_psf.in', 'r').readlines()
    jitxList = np.arange(0,50,10)
    jityList = np.arange(0,50,10)
    disList = np.arange(2.5, 3.5, 0.2) #fix displacement at 3.0
    for angle in [0, 1]:
        for dither in range(4):
            for jitx in jitxList:
                for jity in jityList:
                    for dis in disList:
                        aimDIR = os.path.join('.','PSF', 'angle_{0}_dither_{1}'.format(angle, dither))
                        if not os.path.exist(aimDIR): os.mkdir(aimDIR)
                        modFile = modifyIn(inFile, angle, dither, jitx, jity, dis)
                        fn = modFile[1].strip()+'00.fits'
                        psf_fn = modFile[1].strip()+'00_psf.fits'
                        tt3_fn = modFile[1].strip()+'.tt3'
                        out = open('temp.in', 'w')
                        out.writelines(modFile)
                        out.close()
                        sp.call(['tiny2', 'temp.in'])
                        sp.call(['tiny3', 'temp.in', 'sub=10'])
                        os.remove(psf_fn)
                        os.rename(fn, os.path.join(aimDIR, fn))
