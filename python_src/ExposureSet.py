import numpy as np
from os import path
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pickle
from brewer2mpl import get_map
from HSTFile import HSTFile

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
                self.plotPixel(dim0_i, dim1_i, chisqList, plotDIR)

    def plotPixel (self, dim0, dim1, chisqList, plotDIR = '.'):
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

    def save (self, direction, decorator = 'expSet'):
        """
        save the HSTfile class to pickle file
        """
        with file(path.join(direction,  'Orbit{0}_Exp{1:2d}'.format(self.orbit, self.nExpo) + decorator + '.pkl'), 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load (fn):
        """
        load the saved pickle file
        """
        with file(fn, 'rb') as f:
            return pickle.load(f)