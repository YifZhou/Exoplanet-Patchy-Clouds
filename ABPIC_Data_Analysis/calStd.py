import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy as np

if __name__ == '__main__':
    fn = sys.argv[1]


    df = pd.read_csv(fn, parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    try:
        cosmicRayFN = sys.argv[2]
        cosmicRayDF = pd.read_csv(cosmicRayFN, parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
        df['FLUX'][np.where(np.isnan(cosmicRayDF['FLUX']))[0]] = np.nan
        print len(np.where(np.isnan(cosmicRayDF['FLUX']))[0]), len(df)
    except IndexError:
        pass
    """
    normalize not only by filter, but by rolling angle
    """
    fig, ax = plt.subplots()
    df['FLUX0'] = df['FLUX']
    df.loc[(df['FILTER'] == 'F125W'), 'FLUX0'] = df[(df['FILTER'] == 'F125W')]['FLUX']/df[(df['FILTER'] == 'F125W')]['FLUX'].mean()
    df.loc[(df['FILTER'] == 'F125W') & (df['POSANG'] == 129), 'FLUX0'] = df[(df['FILTER'] == 'F125W') & (df['POSANG'] == 129)]['FLUX']/df[(df['FILTER'] == 'F125W') & (df['POSANG'] == 129)]['FLUX'].mean()
    df.loc[(df['FILTER'] == 'F160W'), 'FLUX0'] = df[(df['FILTER'] == 'F160W')]['FLUX']/df[(df['FILTER'] == 'F160W')]['FLUX'].mean()
    df.loc[(df['FILTER'] == 'F160W') & (df['POSANG'] == 129), 'FLUX0'] = df[(df['FILTER'] == 'F160W') & (df['POSANG'] == 129)]['FLUX']/df[(df['FILTER'] == 'F160W') & (df['POSANG'] == 129)]['FLUX'].mean()
    df['ERR0'] = df['FLUXERR']/df['FLUX']
    df['Time'] = np.float32(df.index.values - df.index.values[0])/(60 * 60 * 1e9) #time in ns

    subdf = df[(df['ORBIT'] >= 10)]
    print subdf[(subdf['FILTER'] == 'F125W')]['FLUX0'].std()
    print subdf[(subdf['FILTER'] == 'F160W')]['FLUX0'].std()