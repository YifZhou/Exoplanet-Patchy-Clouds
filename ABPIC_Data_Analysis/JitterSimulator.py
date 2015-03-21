import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('../python_src')
from linearFit import linearFit

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
    def __init__(self, size, nSamp, p2pDiff = 0.05, fluctuate = 0):
        self.size = size
        self.nSamp = nSamp
        intraPixDim1 = np.sin(np.pi/nSamp * np.arange(nSamp))
        intraPixDim2 = intraPixDim1[:, np.newaxis]
        pixel = np.ones([nSamp, nSamp]) * (1 - p2pDiff) + intraPixDim1 * intraPixDim2 * p2pDiff
        fluctuate = (np.ones([size, size]) + fluctuate*np.random.randn(size, size)).repeat(nSamp, axis = 0).repeat(nSamp, axis = 1)
        
        self.supCCD = np.tile(pixel, [size, size]) * np.abs(fluctuate)#CCD with fine Structure
        self.supRecord = np.zeros([size*nSamp, size*nSamp]) #super sampled result
        self.expTime = 0

    def reset(self):
        """
        reset CCD
        """
        self.expTime = 0
        self.record = np.zeros([self.size, self.size])
        self.supRecord = np.zeros([self.size*self.nSamp, self.size*self.nSamp]) #super sampled result

    def exposure(self, jit, fwhm, jit0 = [0,0], amp = 1.0, time = 3.0):
        """
        one exposure, add one gaussian
        jitV2 : jit[0]
        jitV3 : jit[1]
        jitx0 : jit0[0]
        jity0 : jit0[0]
        """
        plateScale = 0.13 #arcsec/pixel
        jitX = -(jit[1] * np.cos(45) - jit[0] * np.sin(45))/plateScale + jit0[0]
        jitY = -(jit[1] * np.cos(45) + jit[0] * np.sin(45))/plateScale + jit0[1]

        center = [self.size*self.nSamp/2. + jitX*nSamp, self.size*self.nSamp/2. + jitY*nSamp]
        #print [c/nSamp for c in center]
        self.supRecord += self.supCCD * Gaussian2d(self.size*self.nSamp, fwhm*self.nSamp, center) * amp * time
        self.expTime += time

    def read(self):
        """
        read the record out
        rebin the data
        """
        return self.supRecord.reshape((self.size, self.nSamp, self.size, self.nSamp)).sum(axis = 3).sum(axis = 1)/self.expTime


def plotTrend (dataStack, xCenter, side = 2, output = None):#2side+1 x 2side+1 pixels subimage
    plt.close('all')
    fig, axes = plt.subplots(ncols = 2*side + 1, nrows = 2*side + 1, sharex = True, sharey = True, figsize = (24, 20))
    fig.subplots_adjust(hspace = 0, wspace = 0)
    subIMShape = dataStack.shape
    c = subIMShape[0]//2
    delta = xCenter - xCenter[0]
    for i, dim0 in enumerate(range(c-side, c+side+1)):
        for j, dim1 in enumerate(range(c-side, c+side+1)):
            y = dataStack[dim0, dim1, :]/dataStack[dim0, dim1, :].mean()
            b, m, db, dm, chisq = linearFit(delta, y)
            axes[i, j].plot(delta, y, linewidth = 0, marker = '.', label = '({0}, {1})')
            axes[i, j].plot(np.sort(delta), np.sort(delta)*m + b)
            axes[i, j].annotate('x={0},y={1}'.format(dim1 - c, dim0 - c), xy = (0.2, 0.8), xycoords = 'axes fraction')
            axes[i, j].xaxis.set_major_locator(plt.MaxNLocator(4))
            axes[i, j].set_ylim([0.5, 1.5])

            
    if output is None:
        pass
    else:
        plt.savefig(output)
        
if __name__ == '__main__':
    size = 11
    nSamp = 50
    wfc3 = CCD(size, nSamp, 0.1, fluctuate = 0.1)
    df = pd.read_csv('jitter_info.csv', parse_dates = 'time', index_col = 'time')
    expoDF = pd.read_csv('2015_Feb_27_myfits_aper=5_result.csv')
    orbit = 11
    filterName = 'F160W'
    fwhm = 1.10
    subdf = df[(df['orbit'] == orbit) & (df['filter'] == filterName)]
    subExpoDF = expoDF[(expoDF['ORBIT'] == orbit) & (expoDF['FILTER'] == filterName)]
    jitx0 = subExpoDF['XCENTER'].values - np.round(subExpoDF['XCENTER'].values[0])
    jity0 = subExpoDF['YCENTER'].values - np.round(subExpoDF['YCENTER'].values[0])
    fnList = list(set(subdf['file name'].values))
    fnList.sort()
    expStack = np.zeros((size, size, len(fnList)))
    lc = np.zeros(len(fnList))
    time = np.zeros(len(fnList))
    for i, fn in enumerate(fnList):
        fndf = subdf[subdf['file name'] == fn]
        time[i] = fndf.index.values[0]
        for jitV2, jitV3 in zip(fndf['jitter V2'].values, fndf['jitter V3'].values):
            if np.isnan(jitV2) or np.isnan(jitV3): continue
            wfc3.exposure([jitV2, jitV3], fwhm, jit0 = [jitx0[i], jity0[i]])


        expStack[:,:, i] = wfc3.read()
        lc[i] = expStack[:,:, i].sum()
        wfc3.reset()

    plotTrend(expStack, time/(1e9*60))
    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot(111)
    ax2.plot(time, lc/lc.mean())
    ax2.set_xlabel('time (min)')
    ax2.set_ylabel('normalized flux')
    ax2.set_ylim([0.98, 1.02])
    plt.show()