#! /usr/bin/env python
import glob
from astropy.io import fits
import os

def getExposureNo(file_list):
    """
    get the number of exposure
    """
    return [int(item[4:6]) for item in file_list]

def getSubExposureNo(filter_list, expo_list):
    """
    get sub exposure number
    """
    filter0 = filter_list[0]
    expo0 = expo_list[0]
    sub_list = []
    subNo = 1
    for filter_i,expo_i in zip(filter_list, expo_list):
        if filter_i == filter0 and expo_i == expo0:
            sub_list.append(subNo)
        elif filter_i != filter0 and expo_i == expo0:
            subNo += 1
            filter0 = filter_i
            sub_list.append(subNo)
        else:
            subNo = 1
            filter0 = filter_i
            expo0 = expo_i
            sub_list.append(subNo)


    return sub_list

if __name__ == '__main__':
    aimDir = './2M1207A'
    file_list = []
    header_list = []
    angle_list = []
    filter_list = []
    date_list = []
    time_list = []
    exposureTime = []
    for fits_file in sorted(glob.glob(os.path.join(aimDir, '*flt.fits'))):
        fits_content = fits.open(fits_file)
        file_list.append(fits_file.split('/')[-1])
        header = fits_content[0].header
        header_list.append(header)
        angle_list.append(header['PA_V3'])
        filter_list.append(header['filter'])
        date_list.append(header['date-obs'])
        time_list.append(header['time-obs'])
        exposureTime.append(header['exptime'])
        fits_content.close()

    exposureNo = getExposureNo(file_list)
    subExposureNo = getSubExposureNo(filter_list, exposureNo)
    fmt_str = '{0:<20} {1:<2d} {2:<2d} {3:<8} {4:<12} {5:<12} {6:<3.4f} {7:<3.4f}\n'
    output = open(os.path.join(aimDir, 'flt_file_list.dat'), 'w')
    for i in range(len(file_list)):
        output.write(fmt_str.format(file_list[i], exposureNo[i], subExposureNo[i], filter_list[i], date_list[i], time_list[i], angle_list[i], exposureTime[i]))

    output.close()
    #write output


    

    
    
        