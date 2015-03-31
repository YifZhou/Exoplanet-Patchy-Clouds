import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy as np
if __name__ == '__main__':
    fn = sys.argv[1]
    df = pd.read_csv(fn, parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    """
    normalize not only by filter, but by rolling angle
    """
    fig, ax = plt.subplots()
    df['FLUX0'] = df['FLUX']
    df.loc[(df['FILTER'] == 'F125W') & (df['POSANG'] == 101), 'FLUX0'] = df[(df['FILTER'] == 'F125W') & (df['POSANG'] == 101)]['FLUX']/df[(df['FILTER'] == 'F125W') & (df['POSANG'] == 101)]['FLUX'].mean()
    df.loc[(df['FILTER'] == 'F125W') & (df['POSANG'] == 129), 'FLUX0'] = df[(df['FILTER'] == 'F125W') & (df['POSANG'] == 129)]['FLUX']/df[(df['FILTER'] == 'F125W') & (df['POSANG'] == 129)]['FLUX'].mean()
    df.loc[(df['FILTER'] == 'F160W') & (df['POSANG'] == 101), 'FLUX0'] = df[(df['FILTER'] == 'F160W') & (df['POSANG'] == 101)]['FLUX']/df[(df['FILTER'] == 'F160W') & (df['POSANG'] == 101)]['FLUX'].mean()
    df.loc[(df['FILTER'] == 'F160W') & (df['POSANG'] == 129), 'FLUX0'] = df[(df['FILTER'] == 'F160W') & (df['POSANG'] == 129)]['FLUX']/df[(df['FILTER'] == 'F160W') & (df['POSANG'] == 129)]['FLUX'].mean()
    df['ERR0'] = df['FLUXERR']/df['FLUX']
    df['Time'] = np.float32(df.index.values - df.index.values[0])/(60 * 60 * 1e9) #time in ns

    subdf = df[df['ORBIT'] >= 10]
    subdf['Time'] = subdf['Time'] - subdf['Time'].values[0]
    ax.errorbar(subdf[subdf['FILTER'] == 'F125W']['Time'], subdf[subdf['FILTER'] == 'F125W']['FLUX0'], yerr = subdf[subdf['FILTER'] == 'F125W']['FLUX0'] * subdf[subdf['FILTER'] == 'F125W']['ERR0'], fmt = '.', label = 'F125W, Std Dev: {0:.2f}%'.format(subdf[subdf['FILTER'] == 'F125W']['FLUX0'].std() * 100))
    ax.errorbar(subdf[subdf['FILTER'] == 'F160W']['Time'], subdf[subdf['FILTER'] == 'F160W']['FLUX0'] + 0.03, yerr = subdf[subdf['FILTER'] == 'F160W']['FLUX0'] * subdf[subdf['FILTER'] == 'F160W']['ERR0'], fmt = '.', label = 'F160W, Std Dev: {0:.2f}%'.format(subdf[subdf['FILTER'] == 'F160W']['FLUX0'].std() * 100))
    ax.axhline(y = 1.0, linestyle = '--', color = '0.2', linewidth = 0.8)
    ax.axhline(y = 1.03, linestyle = '--', color = '0.2', linewidth = 0.8)
    ax.legend(loc = 'upper right')
    ax.set_ylabel('Normalized Flux', fontsize = 18, fontweight = 'semibold')
    ax.set_xlabel('Time (h)', fontsize = 18, fontweight = 'semibold')
    ax.set_title('HST/WFC3 Photometry of AB Pic b', fontsize = 18, fontweight = 'semibold')
    plt.show()
    #plt.savefig('light_curve.ps')