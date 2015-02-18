from astropy.io import fits
import numpy as np
from os import path
from scipy.optimize import curve_fit

class HSTFile:
    """
    ima file object, parameters:
    filename:
    nSamp
    peakPos
    countArray
    dqarray
    fitCountArray
    side
    """
    def __init__ (self, fileID, peakPos, size):
        """
        initialize ImaFile Object
        """
        self.dataDIR = '/Users/ZhouYf/Documents/Exoplanet-Patchy-Clouds/data/ABPIC-B'
        self.fltFileName = fileID + '_flt.fits'
        self.imaFileName = fileID + '_ima.fits'
        self.dim0 = round(peakPos[0]) 
        self.dim1 = round(peakPos[1]) # dim0 is y, dim1 is x, position is in IMA file coordinate
        self.size = size
        imaFile = fits.open(path.join(self.dataDIR, self.imaFileName))
        self.nSamp = imaFile['primary'].header['nsamp']
        self.countArray = np.zeros([2*size + 1, 2*size + 1, self.nSamp - 1])
        self.dqArray = np.zeros([2*size + 1, 2*size + 1, self.nSamp - 1], dtype = np.int32)
        self.expTime = np.zeros(self.nSamp - 1) #exlucde zeroth read
        for samp_i in range(self.nSamp - 1): # in _ima file, data stored in a backward way, in this object, change it back
            self.expTime[samp_i] = imaFile['sci', self.nSamp - 1 - samp_i].header['samptime']
            self.countArray[:, :, samp_i] = imaFile['sci', self.nSamp - 1 - samp_i].data[self.dim0 - self.size : self.dim0 + self.size + 1, self.dim1 - self.size : self.dim1 + self.size + 1] *\
                                            imaFile['sci', self.nSamp - 1 - samp_i].header['samptime'] # convert countrate into count
            self.dqArray[:, :, samp_i] = imaFile['dq', self.nSamp - 1 - samp_i].data[self.dim0 - self.size : self.dim0 + self.size + 1, self.dim1 - self.size : self.dim1 + self.size + 1]

        self.isSaturated = (self.dqArray / 256 % 2).astype(bool)
        self.isCosmicRay = (self.dqArray / 8192 % 2).astype(bool)
        self.needCorrect = np.any(self.isCosmicRay, axis = 2) + np.any(self.isSaturated, axis = 2)
        imaFile.close()
        fltFile = fits.open(path.join(self.dataDIR, self.fltFileName))
        self.fltCountArray = fltFile['sci'].data[self.dim0 - 5 - size: self.dim0 - 5 + size + 1,
                                                 self.dim1 - 5 - size: self.dim1 - 5 + size + 1] # for flt file coordiate, each dimension needs to be subtracted by 5
        self.fitCountArray = self.fltCountArray.copy()
        fltFile.close()
        self.isCorrected = False

    def correct (self):
        """
        linear fit
         ignoring cosmic ray flag, but exclude the saturated pixels
        """
        badDim0, badDim1 = np.where(self.needCorrect)
        for dim0, dim1 in zip(badDim0, badDim1):
            def func(x, *p):
                return x * p[0] + p[1]
            effIndex = np.where(~self.isSaturated[dim0, dim1, :]) # exclude saturated data
            paras, pcov = curve_fit(func, self.expTime[effIndex], self.countArray[dim0, dim1, :][effIndex], p0 = [self.countArray[dim0, dim1, -1]/self.expTime[-1], 0], sigma = np.sqrt(np.abs(self.countArray[dim0, dim1, :][effIndex])), absolute_sigma = True)
            self.fitCountArray[dim0, dim1] = paras[0]
        self.isCorrected = True

    def to_fits (self, direction, decrator = 'myfits'):
        """
        save the corrected result to fits file
        """
        pass
        

class ExposureSet:
    """
    Exopsure Set object
    Parameters:
    fnList
    center position
    orbit
    expousre number
    filter
    """
    def __init__ (self, fnList, peakPos, orbit, filterName, size = 5):
        """
        initialize Exopusre set object
        """
        self.fnList = fnList
        self.nFile = len(fnList)
        self.orbit = orbit
        self.filterName = filterName
        self.peakPos = peakPos # dim0 is y, dim1 is x, position is in IMA file coordinate
        self.size = 5
        self.HSTFileList = []
        for fn in self.fnList:
            self.HSTFileList.append(HSTFile(fn, self.peakPos, self.size))
            
        self.isCorrected = np.zeros([2*size + 1, 2*size + 1, self.nFile], dtype = bool)
        self.correctedStack = np.zeros([2*size + 1, 2*size + 1, self.nFile])
        
    def correct (self):
        """
        do correction for all HST File Object
        """
        for i, item in enumerate(self.HSTFileList):
            item.correct()
            self.isCorrected[:, :, i] = item.needCorrect
            self.correctStack[:, :, i] = item.fitCountArray

    def testCorrection (self):
        """
        test if the correction is correct
        """
        pass

    def saveFITS(self, direction):
        """
        save the correction into fits file
        """    
        for item in enumerate(self.HSTFileList):
            item.to_fits(direction, decorator = 'myfits')

if __name__ == '__main__':
    test = HSTFile('icdg10vaq', [227, 134], 6)        
    test.correct()