#! /usr/bin/env python
import subprocess as sp
import numpy as np
import os
"""
Use Tinytim to generate a PSFs
"""

aimDIR = './PSFs/'
def modifyIn(inFile, jitx, jity, secDis):
    inFile[1] = 'Jitx_{0:0>2d}_Jity_{1:0>2d}_Dis_{2:.2f}_\n'.format(jitx, jity, secDis)
    inFile[9] = '{0:.5f} # Major axis jitter in mas\n'.format(jitx)
    inFile[10] = '{0:.5f} # Major axis jitter in mas\n'.format(jity)
    inFile[251] = '{0:.5f} #z4 = Focus\n'.format(secDis/100.)
    return inFile

if __name__ == '__main__':
    inFile = open('2mass_psf.in', 'r').readlines()
    jitxList = range(0,80,10)
    jityList = range(0,80,10)
    disList = np.arange(2.6, 2.9, 0.05) #fix displacement at 3.0
    for jitx in jitxList:
        for jity in jityList:
            for dis in disList: 
                modFile = modifyIn(inFile, jitx, jity, dis)
                fn = modFile[1].strip()+'00.fits'
                psf_fn = modFile[1].strip()+'00_psf.fits'
                tt3_fn = modFile[1].strip()+'.tt3'
                out = open('temp.in', 'w')
                out.writelines(modFile)
                out.close()
                sp.call(['tiny2', 'temp.in'])
                sp.call(['tiny3', 'temp.in', 'sub=10'])
                os.remove(psf_fn)
                os.remove(tt3_fn)
                os.rename(fn, os.path.join(aimDIR, fn))



    