import pickle
import pandas as pd
import numpy as np
import glob
import sys
sys.path.append('../python_src')
from linearFit import linearFit
"""
new photometry method, do the up the ramp fit after sum up all pixel values in one read out
"""

if __name__ == '__main__':
    pklList = glob.glob('../data/ABPIC-B_myfits/icdg*pkl')
    pklList.sort()
    size = 5# measure the photometry from a size= box
    chisqTh = 3.0
    flux = np.zeros(len(pklList))
    fluxerr = np.zeros(len(pklList))
    for i, fn in enumerate(pklList):
        hst = pickle.load(open(fn, 'rb'))
        imShape = hst.countArray.shape[:-1] # the last dimension in shape list is the number of samples. First two dimensions are the size of the image for prepared for correction
        nSampEff = hst.nSamp - int(np.any(hst.isSaturated[:, :, -1])) # if the laster read out has a saturated pixel, ignore the last readout
        readoutList = np.zeros(nSampEff-1)
        errorList = np.zeros(nSampEff-1)
        for iSamp in range(nSampEff-1):
            readoutList[iSamp] = np.sum(hst.countArray[imShape[0]//2 - size/2:imShape[0]//2 + size/2 + 1, imShape[0]//2 - size/2:imShape[0]//2 + size/2 + 1, iSamp])
            errorList[iSamp] = np.sqrt(np.sum(hst.errArray[imShape[0]//2 - size/2:imShape[0]//2 + size/2 + 1, imShape[0]//2 - size/2:imShape[0]//2 + size/2 + 1, iSamp]**2))
        b, m, sigb, sigm, chisq = linearFit(hst.expTime[0:nSampEff - 1], readoutList, errorList)
        # if chisq > chisqTh:
        #     flux[i] = np.nan
        #     fluxerr[i] = np.nan
        # else:
        #     flux[i] = readoutList[-1]/hst.expTime[nSampEff - 2]
        #     fluxerr[i] = errorList[-1]/hst.expTime[nSampEff - 2]
        flux[i] = readoutList[-1]/hst.expTime[nSampEff - 2]
        fluxerr[i] = errorList[-1]/hst.expTime[nSampEff - 2]
        print fn, chisq, flux[i]

    df = pd.read_csv('2015_Feb_27_myfits_aper=5_result.csv')
    df['FLUX'] = flux
    df['FLUXERR'] = fluxerr
    df.to_csv('totalRampUp_result.csv', index = False)









