#! /usr/bin/env python
import sys
sys.path.append('../python_src')
from CCD import CCD
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    size = 11
    nSamp = 50
    fwhm = 1.20
    wfc3 = CCD(size, nSamp, 0.1, fluctuate = 0.1)
    df = pd.read_csv('jitter_info.csv', parse_dates = 'time', index_col = 'time')
    fileList = ['icdg10urq', 'icdg10usq', 'icdg10utq', 'icdg10uuq']
    expCubeList = []
    for fn_index, fn in enumerate(fileList):
        subdf = df[df['file name'] == fn]
        t = np.float32(subdf.index.values - subdf.index.values[0])/(1e9)
        expCube = np.zeros((size, size, 9))
        jitx0 = t/3600 * 0.01070+0.20# shift speed by linear fit
        jity0 = t/3600 * 0.12363+0.15# shift speed by linear fit
        jitV2 = subdf['jitter V2'].values
        jitV3 = subdf['jitter V3'].values
        for i in range(1,10):
            if (np.isnan(jitV2[i])) or (np.isnan(jitV3[i])): continue
            wfc3.exposure([jitV2[i], jitV3[i]], fwhm, jit0 = [jitx0[i], jity0[i]])
            expCube[:,:,i-1] = wfc3.sample()
        meanX = -(jitV3.mean() * np.cos(np.pi/4) - jitV2.mean()* np.cos(np.pi/4))/0.13
        meanY = -(jitV3.mean() * np.cos(np.pi/4) + jitV2.mean()* np.cos(np.pi/4))/0.13

        print fn, meanX, meanY
        expCubeList.append(expCube.copy())
        wfc3.reset()

    t0 = t[1:10]
    x0 = 6
    y0 = 5
    for i in range(4):
        plt.plot(t0, expCubeList[i][x0, y0, :], '.')

    plt.show()