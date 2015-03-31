from os import path, mkdir
import sys
sys.path.append('../python_src')
import pandas as pd
from ExposureSet import ExposureSet


if __name__ == '__main__':
    df = pd.read_csv('ABPIC-B_imaInfo4Calibration.csv')
    dataDIR = './ABPIC-B/'
    for orbit in range(7, 13):
        for nExpo in range(13):
            plotDIR = path.join('./ABPIC-B_myfits','orbit_{0}_expo_{1}'.format(orbit,nExpo))
            if not path.exists(plotDIR): mkdir(plotDIR)
            subdf = df[(df['orbit'] == orbit) & (df['exposure set'] == nExpo)]
            exp = ExposureSet(subdf['file ID'].values, dataDIR,[subdf['YCENTER'].values[0], subdf['XCENTER'].values[0]] , orbit, nExpo, subdf['filter'].values[0])
            exp.correct(correctAll = True, chisqTh = 2.5)
            exp.testCorrection2(chisqTh = 3, doPlot = True, plotDIR = plotDIR)
            exp.saveFITS('./ABPIC-B_myfits')
            exp.savePickle('./ABPIC-B_myfits')