#! /usr/bin/env python
"""
gather file info for one specific type of file
columns are: file name, filter, observation Time, orbit, dither position
"""
import glob
from astropy.io import fits
import os
import pandas as pd
import numpy as np
from math import floor

def getTargetNo(file_list):
    """
    get the target number
    """
    return [int(item[4:6]) for item in file_list]

def createInfoFile(dataDir, fileType, saveDir = '.'):
    # dataDir = '../data'
    # target = '2M1207-B'
    # fileType = 'flt'
    file_list = []
    angle_list = []
    filter_list = []
    date_list = []
    time_list = []
    exposureTime = []
    orbitNo = []
    ditherNo = []
    exposureNo = []
    
    for fits_file in sorted(glob.glob(os.path.join(dataDir, '*{0}.fits'.format(fileType)))):
        fits_content = fits.open(fits_file)
        file_list.append(fits_file.split('/')[-1])
        header = fits_content[0].header
        angle_list.append(round(header['PA_V3']))
        filter_list.append(header['filter'])
        date_list.append(header['date-obs'])
        time_list.append(header['time-obs'])
        exposureTime.append(header['exptime'])
        targOff1 = floor(header['postarg1'])
        targOff2 = floor(header['postarg2']) * 2 # so that dither number could be expressed as targOff1 + tarOff2
        ditherNo.append(int(targOff1 + targOff2))
        fits_content.close()

    orbitNo = getTargetNo(file_list)
    filter0 = filter_list[0]
    orbit0 =  orbitNo[0]
    exposure0 = 0
    for filter_i, orbit_i in zip(filter_list, orbitNo):
        if filter_i == filter0 and orbit_i == orbit0:
            exposureNo.append(exposure0)
        elif filter_i != filter0 and orbit_i == orbit0:
            exposure0 += 1
            filter0 = filter_i
            exposureNo.append(exposure0)
        else:
            exposure0 = 0
            filter0 = filter_i
            orbit0 = orbit_i
            exposureNo.append(exposure0)

    fileInfo = pd.DataFrame([line for line in zip(file_list, filter_list, orbitNo, angle_list, ditherNo, exposureNo, date_list, time_list, exposureTime)],
                            columns = ['file name', 'filter', 'orbit', 'Pos Angle', 'dither', 'exposure set', 'obs date', 'obs time', 'exposure time'])
    fileInfo.to_csv('ABPIC-B_{0}_fileInfo.csv'.format(fileType), index = False)

def createInfoFileFromResult(infoFn, resultFn, outfn):
    """
    create infofile for data recalibration pipeline
    add xc and yc column for original data frame
    change filename into file indentifier
    """
    infoDF = pd.read_csv(infoFn)
    resultDF = pd.read_csv(resultFn)
    infoDF['XCENTER'] = np.round(resultDF['XCENTER'])
    infoDF['YCENTER'] = np.round(resultDF['YCENTER'])
    infoDF = infoDF.rename(columns = {'file name': "file ID"})
    infoDF['file ID'] = [filename.split('_')[0] for filename in infoDF['file ID']]
    infoDF.to_csv(outfn, index = False)
    
if __name__ == '__main__':
    createInfoFile('../data/ABPIC-B/', 'drz')