import glob
from astropy.io import fits
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def CentralPixel (DF, nPixel = 1):
    """
    plot central value, show if it has ramp effect
    """
    centralFlux = []
    for index, row in DF.iterrows():
        fitsFile = fits.open('../data/ABPIC-B/' + row['FILENAME'])
        yc, xc = round(row['XCENTER']), round(row['YCENTER'])
        centralFlux.append(np.sort(fitsFile['SCI', 1].data[xc-2: xc + 2, yc - 2: yc + 2].flat)[-1:-1-nPixel:-1].sum())
        fitsFile.close()
    return np.array(centralFlux)

if __name__ == '__main__':
    
    df = pd.read_csv('2015_Jan_07_result.csv', parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    c = CentralPixel(df)
    AVGjit = []
    V2jit = []
    V3jit = []
    jitList = sorted(glob.glob('../data/ABPIC-B/*jit.fits'))
    for jitFN in jitList:
        jit = fits.open(jitFN)
        for ext in range(1, len(jit)):
            V2 = jit[ext].data['SI_V2_AVG']
            V3 = jit[ext].data['SI_V3_AVG']
            V2 = V2[np.abs(V2) < 1.0]
            V3 = V3[np.abs(V3) < 1.0]
            V2jit.append(np.mean(V2))
            V3jit.append(np.mean(V3))

    df["C"] = c
    df['V2jit'] = V2jit
    df['V3jit'] = V3jit
    # plt.close('all')
    # #plt.plot(np.sqrt(df[(df['ORBIT'] == 10) & (df['FILTER'] == 'F125W')]['V2jit']**2 + df[(df['ORBIT'] == 10) & (df['FILTER'] == 'F125W')]['V3jit']**2) , df[(df['ORBIT'] == 10) & (df['FILTER'] == 'F125W')]['C'], '.')
    # subdf = df[(df['ORBIT'] == 10) & (df['FILTER'] == 'F125W')]
    # dx = subdf['XCENTER'] - subdf['XCENTER'].values[0]
    # dy = subdf['YCENTER'] - subdf['YCENTER'].values[0]
    # plt.plot(np.sqrt(dx**2 + dy**2), np.sqrt(subdf['V2jit']**2 + subdf['V3jit']**2), '.')
    # plt.show()