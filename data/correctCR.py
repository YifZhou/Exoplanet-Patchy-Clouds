from astropy.io import fits
import numpy as np
from os import path, mkdir
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd

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
        self.fileID = fileID
        self.fltFileName = self.fileID + '_flt.fits'
        self.imaFileName = self.fileID + '_ima.fits'
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
        fltFile = fits.open(path.join(self.dataDIR, self.fltFileName))
        fltFile['sci'].data[self.dim0 - 5 - self.size: self.dim0 - 5 + self.size + 1,
                            self.dim1 - 5 - self.size: self.dim1 - 5 + self.size + 1]
        fltFile.writeto(path.join(direction, self.fileID + '_' + decrator + '.fits'))
        fltFile.close()

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
    def __init__ (self, fnList, peakPos, orbit, nExpo, filterName, size = 5):
        """
        initialize Exopusre set object
        """
        self.fnList = fnList
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
            self.HSTFileList.append(HSTFile(fn, self.peakPos, self.size))

        self.expTime = self.HSTFileList[0].expTime[-1] # the exposure time for individual file, used for caculating couting uncertainties
        self.isCorrected = np.zeros([2*size + 1, 2*size + 1, self.nFile], dtype = bool)
        self.correctedStack = np.zeros([2*size + 1, 2*size + 1, self.nFile])
        self.problematicPixel = [] #save the coordinates of the pixels that have problematic correction problem
        
    def correct (self):
        """
        do correction for all HST File Object
        """
        for i, item in enumerate(self.HSTFileList):
            item.correct()
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
                    # plot the result for checking
                    plt.close('all')
                    fig, ax = plt.subplots()
                    ax.errorbar(np.arange(len(count)), count, yerr = np.sqrt(np.abs(count)),linewdith = 0 , fmt = '.')
                    ax.plot(np.arange(len(count)), np.arange(len(count)) * paras[0] + paras[1])
                    ax.set_xlabel('Exposure Number')
                    ax.set_ylabe('Count (e$^-$)')
                    ax.set_title('m = {0}, b = {1}'.format(paras[0], paras[1]))
                    plt.savefig(path.join(plotDIR, 'Orbit_{0}_Expo_{1}_x_{2}_y_{3}.pdf'.format(self.orbit, self.nExpo, self.dim1_i, self.dim0_i)))
                    # save filename orbit_i_expo_j_x_xxx_y_yyy.pdf
    

    def saveFITS(self, direction):
        """
        save the correction into fits file
        """    
        for item in enumerate(self.HSTFileList):
            item.to_fits(direction, decorator = 'myfits')

if __name__ == '__main__':
    df = pd.read_csv('ABPIC-B_imaInfo4Calibration.csv')
    for orbit in range(10, 13):
        for nExpo in range(13):
            plotDIR = path.join('./ABPIC-B_myfits','orbit_{0}_expo_{1}'.format(orbit,nExpo))
            if ~path.exists(plotDIR): mkdir(plotDIR)
            subdf = df[(df['orbit'] == orbit) & (df['exposure set'] == nExpo)]
            exp = ExposureSet(subdf['file ID'].values,[subdf['YCENTER'].values[0], subdf['XCENTER'].values[0]] , orbit, nExpo, subdf['filter'].values[0])
            exp.correct()
            exp.testCorrection(doPlot = True, plotDIR = plotDIR)
            exp.saveFITS('./ABPIC-B_myfits')