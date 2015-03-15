import numpy as np
import pandas as pd

def Gaussian2d(size, fwhm = 3, center=None):
    """ Make a square gaussian kernel.

    size is the length of a side of the square
    fwhm is full-width-half-maximum, which
    can be thought of as an effective radius.

    use Gaussian as PSF
    """
 
    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]
    
    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]
    
    return np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)
    
class CCD:
    """
    simulate a HST CCD
    """
    def __init__(self, size, nSamp, p2pDiff = 0.05):
        self.size = size
        self.nSamp = nSamp
        intraPixDim1 = np.sin(np.pi/nSamp * np.arange(nSamp))
        intraPixDim2 = intraPixDim1[:, np.newaxis]
        pixel = np.ones([nSamp, nSamp]) * (1 - p2pDiff) + intraPixDim1 * intraPixDim2 * p2pDiff
        self.supCCD = np.tile(pixel, [size, size]) #CCD with fine Structure
        self.supRecord = np.zeros([size*nSamp, size*nSamp]) #super sampled result
        self.expTime = 0

    def reset(self):
        """
        reset CCD
        """
        self.expTime = 0
        self.record = np.zeros([self.size, self.size])
        self.supRecord = np.zeros([self.size*self.nSamp, self.size*self.nSamp]) #super sampled result

    def exposure(self, jit, fwhm, amp = 1.0, time = 3.0):
        """
        one exposure, add one gaussian
        jitV2 : jit[0]
        jitV3 : jit[1]
        """
        plateScale = 0.13 #arcsec/pixel
        jitX = (jit[1] * np.cos(45) - jit[0] * np.sin(45))/plateScale
        jitY = (jit[1] * np.cos(45) + jit[0] * np.sin(45))/plateScale

        center = [self.size*self.nSamp/2. + jitY*nSamp, self.size*self.nSamp/2. + jitX*nSamp]
        #print [c/nSamp for c in center]
        self.supRecord += self.supCCD * Gaussian2d(self.size*self.nSamp, fwhm*self.nSamp, center) * amp * time
        self.expTime += time

    def read(self):
        """
        read the record out
        rebin the data
        """
        return self.supRecord.reshape((self.size, self.nSamp, self.size, self.nSamp)).sum(axis = 3).sum(axis = 1)/self.expTime

        
if __name__ == '__main__':
    size = 11
    nSamp = 50
    wfc3 = CCD(size, nSamp, 0.1)
    df = pd.read_csv('jitter_info.csv', parse_dates = 'time', index_col = 'time')
    orbit = 10
    filterName = 'F125W'
    fwhm = 1.10
    subdf = df[(df['orbit'] == orbit) & (df['filter'] == filterName)]
    fnList = list(set(subdf['file name'].values))
    fnList.sort()
    expStack = np.zeros((size, size, len(fnList)))
    lc = np.zeros(len(fnList))
    for i, fn in enumerate(fnList):
        fndf = subdf[subdf['file name'] == fn]
        for jitV2, jitV3 in zip(fndf['jitter V2'].values, fndf['jitter V3'].values):
            if np.isnan(jitV2) or np.isnan(jitV3): continue
            wfc3.exposure([jitV2, jitV3], fwhm)


        expStack[:,:, i] = wfc3.read()
        lc[i] = wfc3.read().sum()
        wfc3.reset()
        

