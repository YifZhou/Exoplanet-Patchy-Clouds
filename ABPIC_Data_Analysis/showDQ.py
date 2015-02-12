import numpy as np
from astropy.io import fits
import sys
#import matplotlib.pyplot as plt
import pandas as pd

def dq2Bad(dq, flag):
    return (dq / flag) % 2

def printCRFlag (fnList, nSamp):
    """
    print number of pixels that have CR detection during crcorr
    """
    flag = 8192
    nbad = []
    for fitsfn in fnList:
        nbad[:] = []
        fitsFile = fits.open('../data/ABPIC-B/' + fitsfn)
        for iSamp in range(1, 1 + nSamp):
            badPixelMap = dq2Bad(fitsFile['DQ', iSamp].data, flag)
            nbad.append(np.where(badPixelMap != 0)[0].size)

        fitsFile.close()
        print fitsfn, nbad


def printCREff (DF):
    """
    print CR coordinates that is inside the 
    """
    flag = 8192
    nBad = []
    for index, row in DF.iterrows():
        dq = fits.open('../data/ABPIC-B/' + row['FILENAME'])['DQ', 1].data
        bady, badx = np.where(dq2Bad(dq, flag) != 0)
        inCircle = np.where(np.sqrt((badx - row['XCENTER'])**2 + (bady - row['YCENTER'])**2) < 3)
        print row['FILENAME'], badx[inCircle], bady[inCircle]
        nBad.append(len(badx[inCircle]))
        
    return nBad

def plotBadPixel (fnList, flags):
    """
    plot bad pixel map
    """
    pass
            

if __name__ == '__main__':
    # outFn = sys.argv[1]         
    DF = pd.read_csv('2015_Jan_16_ima_result.csv')
    #concernedFlag = [3, 5, 6, 7, 13, 14]
    concernedFlag = [8192]
    markers = ['x', '+', '.', 's', '3', '4']
    # F125File = DF[DF['FILTER'] == 'F125W']['FILENAME'].values
    # F160File = DF[DF['FILTER'] == 'F160W']['FILENAME'].values
    # printCRFlag(F125File, 6)
    # printCRFlag(F160File, 4)
    nBad = printCREff(DF)
    # DF['CR number'] = nBad
    # DF.to_csv(outFn)
    
#     for fitsfn in F125File:
#         fitsContent = fits.open('../data/ABPIC-B/' + fitsfn)
#         nbad = 0
# #        im = fitsContent['SCI'].data
#         dq = fitsContent['DQ'].data
#         for i, flag in enumerate(concernedFlag):
#             badPixelMap = dq2Bad(dq, flag)
#             x, y = np.where(badPixelMap)
#             print fitsfn, len(x)
#             # ax.plot(y, x, linewidth = 0, marker = markers[i], ms = 4)

#         figName = fitsfn.replace('.fits', '_dq.pdf') 
#         # fig.savefig('./dq/' + figName)
#         # print figName, ' saved'
#         # plt.close(fig)          
#         fitsContent.close()
    