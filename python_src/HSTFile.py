import numpy as np
from os import path
import pickle
from astropy.io import fits

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
    def __init__ (self, fileID, dataDIR, peakPos, size):
        """
        initialize ImaFile Object
        """
        self.dataDIR = dataDIR#'/Users/ZhouYf/Documents/Exoplanet-Patchy-Clouds/data/ABPIC-B'
        self.fileID = fileID
        self.fltFileName = self.fileID + '_flt.fits'
        self.imaFileName = self.fileID + '_ima.fits'
        self.dim0 = round(peakPos[0]) 
        self.dim1 = round(peakPos[1]) # dim0 is y, dim1 is x, position is in IMA file coordinate
        self.size = size
        imaFile = fits.open(path.join(self.dataDIR, self.imaFileName))
        self.nSamp = imaFile['primary'].header['nsamp']
        self.countArray = np.zeros([2*size + 1, 2*size + 1, self.nSamp - 1])
        self.errArray = np.zeros([2*size + 1, 2*size + 1, self.nSamp - 1])
        self.dqArray = np.zeros([2*size + 1, 2*size + 1, self.nSamp - 1], dtype = np.int32)
        self.expTime = np.zeros(self.nSamp - 1) #exlucde zeroth read
        for samp_i in range(self.nSamp - 1): # in _ima file, data stored in a backward way, in this object, change it back
            self.expTime[samp_i] = imaFile['sci', self.nSamp - 1 - samp_i].header['samptime']
            self.countArray[:, :, samp_i] = imaFile['sci', self.nSamp - 1 - samp_i].data[self.dim0 - self.size : self.dim0 + self.size + 1, self.dim1 - self.size : self.dim1 + self.size + 1] *\
                                            imaFile['sci', self.nSamp - 1 - samp_i].header['samptime'] # convert countrate into count
            self.dqArray[:, :, samp_i] = imaFile['dq', self.nSamp - 1 - samp_i].data[self.dim0 - self.size : self.dim0 + self.size + 1, self.dim1 - self.size : self.dim1 + self.size + 1]
            self.errArray[:, :, samp_i] = imaFile['err', self.nSamp - 1 - samp_i].data[self.dim0 - self.size : self.dim0 + self.size + 1, self.dim1 - self.size : self.dim1 + self.size + 1]*\
                                            imaFile['sci', self.nSamp - 1 - samp_i].header['samptime']

        self.isSaturated = (self.dqArray / 256 % 2).astype(bool)
        self.isCosmicRay = (self.dqArray / 8192 % 2).astype(bool)
        self.needCorrect = np.any(self.isCosmicRay, axis = 2) + np.any(self.isSaturated, axis = 2)
        imaFile.close()
        fltFile = fits.open(path.join(self.dataDIR, self.fltFileName))
        pam = fits.getdata('../data/pam.fits') #pixel area map
        self.fltCountArray = fltFile['sci'].data[self.dim0 - 5 - size: self.dim0 - 5 + size + 1,
                                                 self.dim1 - 5 - size: self.dim1 - 5 + size + 1] # for flt file coordiate, each dimension needs to be subtracted by 5
        pamArray = pam[self.dim0 - 5 - size: self.dim0 - 5 + size + 1,
                            self.dim1 - 5 - size: self.dim1 - 5 + size + 1] # same for pixel area map
        for samp_i in range(self.nSamp - 1):
            self.countArray[:, :, samp_i] = self.countArray[:, :, samp_i] * pamArray
        self.fltCountArray = self.fltCountArray * pamArray
        self.fitCountArray = self.fltCountArray.copy()
        self.chisqArray = np.ones([2*size + 1, 2*size + 1]) # array to save the chisq result
        self.zeroValue = np.zeros(self.fltCountArray.shape)
        fltFile.close()
        self.isCorrected = False

    def correct (self, correctAll = False, chisqTh = 5):
        """
        linear fit
         ignoring cosmic ray flag, but exclude the saturated pixels
        """
        badDim0, badDim1 = np.where(self.needCorrect)
        coords = zip(badDim0, badDim1)
        if correctAll: coords = [(dim0, dim1) for dim0 in range(2*self.size + 1) for dim1 in range(2*self.size + 1)]

        for dim0, dim1 in coords:
            effIndex = np.where(~self.isSaturated[dim0, dim1, :]) # exclude saturated data
            x = self.expTime[effIndex]
            y = self.countArray[dim0][dim1][effIndex] 
            dy = self.errArray[dim0][dim1][effIndex] 
            b, m, sigb, sigm, chisq = self.linearFit(x, y, dy)
            if ((chisq > chisqTh) and len(x) > 4) or (chisq > 20 and len(x) > 3): #at least 4 points needed for cosmic ray identification, only identify cosmic ray hit at the beginning or the end of the exposure, or some crazy stuff happend
                b0, m0, chisq0 = b, m, chisq
                b1, m1, sigb1, sigm1, chisq1 = self.linearFit(x[0:-1], y[0:-1], dy[0:-1])
                b2, m2, sigb2, sigm2, chisq2 = self.linearFit(x[1:], y[1:], dy[1:])
                chisq = np.array([chisq0, chisq1, chisq2]).min(axis = -1)
                b = np.array([b0, b1, b2])[np.where(np.array([chisq0, chisq1, chisq2]) == chisq)]
                m = np.array([m0, m1, m2])[np.where(np.array([chisq0, chisq1, chisq2]) == chisq)] #choose the result from the fit that has the least chisq value
            
            self.fitCountArray[dim0, dim1] = m
            self.zeroValue[dim0, dim1] = b
            self.chisqArray[dim0, dim1] = chisq
        self.isCorrected = True

    def linearFit(self, x, y, dy):
        """
        my own linear fit routine, since there is no good scipy or numpy linearFit routine written up
        """
        Y = np.mat(y).T
        A = np.mat([np.ones(len(x)), x]).T
        C = np.mat(np.diagflat(dy**2))
        mat1 = (A.T*C**(-1)*A)**(-1)
        mat2 = A.T*C**(-1)*Y
        b, m = mat1 * mat2
        b = b.flat[0]
        m = m.flat[0]
        sigb, sigm = np.sqrt(np.diag(mat1))
        chisq = 1./(len(x) - 2) * ((y - m * x - b)**2/dy**2).sum(axis = -1)
        return b, m, sigb, sigm, chisq

    def to_fits (self, direction, decorator = 'myfits'):
        """
        save the corrected result to fits file
        """
        fltFile = fits.open(path.join(self.dataDIR, self.fltFileName))
        fltFile['sci'].data[self.dim0 - 5 - self.size: self.dim0 - 5 + self.size + 1,
                            self.dim1 - 5 - self.size: self.dim1 - 5 + self.size + 1] = self.fitCountArray
        fltFile.writeto(path.join(direction, self.fileID + '_' + decorator + '.fits'), clobber = True)
        fltFile.close()

    def save (self, direction, decorator = 'myfits'):
        """
        save the HSTfile class to pickle file
        """
        with file(path.join(direction, self.fileID + '_' + decorator + '.pkl'), 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load (fn):
        """
        load the saved pickle file
        """
        with file(fn, 'rb') as f:
            return pickle.load(f)