from astropy.io import fits
import numpy as np
from os import path, mkdir
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from brewer2mpl import get_map

def linearFit(x, y, dy):
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
            self.errArray[:, :, samp_i] = imaFile['err', self.nSamp - 1 - samp_i].data[self.dim0 - self.size : self.dim0 + self.size + 1, self.dim1 - self.size : self.dim1 + self.size + 1]

        self.isSaturated = (self.dqArray / 256 % 2).astype(bool)
        self.isCosmicRay = (self.dqArray / 8192 % 2).astype(bool)
        self.needCorrect = np.any(self.isCosmicRay, axis = 2) + np.any(self.isSaturated, axis = 2)
        imaFile.close()
        fltFile = fits.open(path.join(self.dataDIR, self.fltFileName))
        self.fltCountArray = fltFile['sci'].data[self.dim0 - 5 - size: self.dim0 - 5 + size + 1,
                                                 self.dim1 - 5 - size: self.dim1 - 5 + size + 1] # for flt file coordiate, each dimension needs to be subtracted by 5
        self.fitCountArray = self.fltCountArray.copy()
        self.chisqArray = self.ones([2*size + 1, 2*size + 1]) # array to save the chisq result
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
            y = self.countArray[dim0, dim1, :] * x
            dy = self.countArray[dim0, dim1, :] * x
            b, m, sigb, sigm, chisq = linearFit(x, y, dy)
            if (chisq > chisqTh) and len(x) > 4: #at least 4 points needed for cosmic ray identification, only identify cosmic ray hit at the beginning or the end of the exposure
                b0, m0, chisq0 = b, m, chisq
                b1, m1, sigb1, sigm1, chisq1 = linearFit(x[0:-1], y[0:-1], dy[0:-1])
                b2, m2, sigb2, sigm2, chisq2 = linearFit(x[1:], y[1:], dy[1:])
                chisq = np.array([chisq0, chisq1, chisq2]).min(axis = -1)
                b = np.array([b0, b1, b2])[np.where(np.array([chisq0, chisq1, chisq2]) == chisq)]
                m = np.array([m0, m1, m2])[np.where(np.array([chisq0, chisq1, chisq2]) == chisq)] #choose the result from the fit that has the least chisq value
            
            self.fitCountArray[dim0, dim1] = m
            self.zeroValue[dim0, dim1] = b
            self.chisqArray = chisq
        # for dim0, dim1 in coords:
        #     def func(x, *p):
        #         return x * p[0] + p[1]
        #     effIndex = np.where(~self.isSaturated[dim0, dim1, :]) # exclude saturated data
        #     paras, pcov = curve_fit(func, self.expTime[effIndex], self.countArray[dim0, dim1, :][effIndex], p0 = [self.countArray[dim0, dim1, -1]/self.expTime[-1], 0], sigma = np.sqrt(np.abs(self.countArray[dim0, dim1, :][effIndex])), absolute_sigma = True)
        #     self.fitCountArray[dim0, dim1] = paras[0]
        #     self.zeroValue[dim0, dim1] = paras[1]
        self.isCorrected = True

    def to_fits (self, direction, decorator = 'myfits'):
        """
        save the corrected result to fits file
        """
        fltFile = fits.open(path.join(self.dataDIR, self.fltFileName))
        fltFile['sci'].data[self.dim0 - 5 - self.size: self.dim0 - 5 + self.size + 1,
                            self.dim1 - 5 - self.size: self.dim1 - 5 + self.size + 1] = self.fitCountArray
        fltFile.writeto(path.join(direction, self.fileID + '_' + decorator + '.fits'))
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
    def __init__ (self, fnList, dataDIR, peakPos, orbit, nExpo, filterName, size = 5):
        """
        initialize Exopusre set object
        """
        self.fnList = fnList
        self.dataDIR = dataDIR
        self.nFile = len(fnList)
        self.orbit = orbit
        self.nExpo = nExpo # exposure number
        self.filterName = filterName
        self.peakPos = peakPos # dim0 is y, dim1 is x, position is in IMA file coordinate
        self.dim0 = peakPos[0]
        self.dim1 = peakPos[1]
        self.size = 5
        self.dim00 = self.dim0 - size
        self.dim10 = self.dim1 - size # define the lower left corner of the region of interest
        
        self.HSTFileList = []
        for fn in self.fnList:
            self.HSTFileList.append(HSTFile(fn, self.dataDIR, self.peakPos, self.size))

        self.expTime = self.HSTFileList[0].expTime[-1] # the exposure time for individual file, used for caculating couting uncertainties
        self.isCorrected = np.zeros([2*size + 1, 2*size + 1, self.nFile], dtype = bool)
        self.correctedStack = np.zeros([2*size + 1, 2*size + 1, self.nFile])
        self.problematicPixel = [] #save the coordinates of the pixels that have problematic correction problem
        
    def correct (self, correctAll = False, chisqTh = 5):
        """
        do correction for all HST File Object
        """
        for i, item in enumerate(self.HSTFileList):
            item.correct(correctAll = correctAll, chisqTh = chisqTh)
            self.isCorrected[:, :, i] = item.needCorrect
            self.correctedStack[:, :, i] = item.fitCountArray

        print 'Orbit {0}, Exposure {1} finished re-calibration'.format(self.orbit, self.nExpo)

    def testCorrection (self, sigmaThreshold = 3, doPlot = False, plotDIR = "."):
        """test if the correction is correct
        test method: assume that
        in short time scale (within in a exposure set ~10 min), the
        count rate of one pixel changes linearly.  Thus for every
        corrected pixel, this routine do a linear fit within a
        exposure set and exclude the pixel that is specified sigma
        away (default is 5 sigma) from the lienar fit.

        """
        self.problematicPixel[:] = []
        dim0, dim1 = np.where(np.any(self.isCorrected, axis = 2)) # the coordinate of the pixel that has calibration correction made
        for dim0_i, dim1_i in zip(dim0, dim1):
            count = self.expTime * self.correctedStack[dim0_i, dim1_i, :]
            def func(x, *p):
                return x * p[0] + p[1]
                
            paras, pcov = curve_fit(func, np.arange(len(count)), count, p0 = [1., count[0]], sigma = np.sqrt(np.abs(count)), absolute_sigma = True) # since exposures are equally sampled, use arange(nsamp) as x index
            diff = np.abs(paras[0] * np.arange(len(count)) + paras[1] - count)/np.sqrt(np.abs(count))
            problematicIndex = np.where(diff > sigmaThreshold)[0]
            self.problematicPixel += [(dim0_i, dim1_i, pid) for pid in problematicIndex]
            for pid in problematicIndex:
                print 'exposure {0} has problematics correction at ({1}, {2})'.format(self.fnList[pid], dim0_i +self. dim00, dim1_i + self.dim10)
                
            if doPlot:
                self.plotPixel(dim0_i, dim1_i)

    def testCorrection2 (self, chisqTh = 5, doPlot = False, plotDIR = "."):
        """test if the correction is correct
        plot out the pixel that has a bad up the ramp fit,
        the quality of the fit is defined by chisq valeu
        """
        self.problematicPixel[:] = []
        chisqList = np.ones(len(self.HSTFileList))
        dim0, dim1 = np.where(np.any(self.isCorrected, axis = 2)) # the coordinate of the pixel that has calibration correction made
        for dim0_i, dim1_i in zip(dim0, dim1):
            for i in range(len(chisqList)): chisqList[i] = self.HSTFileList[i].chisqArray[dim0_i, dim1_i]
            problematicIndex = np.where(chisqList > chisqTh)[0]
            self.problematicPixel += [(dim0_i, dim1_i, pid) for pid in problematicIndex]
            for pid in problematicIndex:
                print 'exposure {0} has problematics correction at ({1}, {2})'.format(self.fnList[pid], dim0_i +self. dim00, dim1_i + self.dim10)
                
            if doPlot:
                self.plotPixel(dim0_i, dim1_i, chisqList)

    def plotPixel (self, dim0, dim1, chisqList):
        """
        plot the up-the-ramp fit for a problematic pixel
        """
        colors = get_map('Set1', 'Qualitative', 5).mpl_colors
        plt.close('all')
        fig, ax = plt.subplots()
        for exp_id, exposure in enumerate(self.HSTFileList):
            ax.errorbar(exposure.expTime, exposure.countArray[dim0, dim1, :], yerr = np.sqrt(np.abs(exposure.countArray[dim0, dim1, :])),linewidth = 0 , fmt = 'o', color = colors[exp_id])
            ax.plot(exposure.expTime, exposure.expTime * exposure.fitCountArray[dim0, dim1] + exposure.zeroValue[dim0, dim1], color = colors[exp_id], label = 'exp {0}, chisq = {1}'.format(exp_id, chisqList[exp_id]))
        
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Count (e$^-$)')
        ax.set_title('x = {0}, y = {1}'.format(self.dim10 + dim1, self.dim00 + dim0))
        ax.legend(loc = 'best')
        plt.savefig(path.join(plotDIR, 'Orbit_{0}_Expo_{1}_x_{2}_y_{3}.pdf'.format(self.orbit, self.nExpo, self.dim10 + dim1, self.dim00 + dim0)))

    def saveFITS(self, direction):
        """
        save the correction into fits file
        """    
        for item in self.HSTFileList:
            item.to_fits(direction, decorator = 'myfits')

    def savePickle (self, direction):
        """
        save ima object into pickle file
        """
        for item in self.HSTFileList:
            item.save(direction, decorator = 'myfits')

if __name__ == '__main__':
    df = pd.read_csv('ABPIC-B_imaInfo4Calibration.csv')
    dataDIR = './ABPIC-B/'
    for orbit in range(10, 13):
        for nExpo in range(13):
            plotDIR = path.join('./ABPIC-B_myfits','orbit_{0}_expo_{1}'.format(orbit,nExpo))
            if not path.exists(plotDIR): mkdir(plotDIR)
            subdf = df[(df['orbit'] == orbit) & (df['exposure set'] == nExpo)]
            exp = ExposureSet(subdf['file ID'].values, dataDIR,[subdf['YCENTER'].values[0], subdf['XCENTER'].values[0]] , orbit, nExpo, subdf['filter'].values[0])
            exp.correct(correctAll = True, chisqTh = 5)
            exp.testCorrection2(chisqTh = 3, doPlot = True, plotDIR = plotDIR)
            exp.saveFITS('./ABPIC-B_myfits')
            exp.savePickle('./ABPIC-B_myfits')