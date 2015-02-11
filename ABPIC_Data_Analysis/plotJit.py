import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
from glob import glob
from astropy.io import fits
import numpy as np

def addSec (time, sec):
    """
    add second to a timebase
    """
    if len(sec) <= 1:
        return time + timedelta(seconds = sec)
    else:
        return [time + timedelta(seconds = sec_i) for sec_i in sec]

if __name__ == '__main__':
    df = pd.read_csv('2015_Jan_16_ima_result.csv', parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    t = iter(df.index)
    jitList = sorted(glob('../data/ABPIC-B/*jit.fits'))
    time = []
    V2jit = []
    V3jit = []
    AVGjit = []
    for jitFN in jitList:
        jit = fits.open(jitFN)
        for ext in range(1, len(jit)):
            time += addSec(next(t), jit[ext].data['Seconds'].tolist())
            V2jit += jit[ext].data['SI_V2_AVG'].tolist()
            V3jit += jit[ext].data['SI_V3_AVG'].tolist()
            AVGjit.append(np.sqrt(np.std(jit[ext].data['SI_V3_AVG'])**2 + np.std(jit[ext].data['SI_V3_AVG'])))

    time = np.array(time)
    V2jit = np.array(V2jit)
    V3jit = np.array(V3jit)

    plt.close('all')
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(time, V2jit, label = 'V2 axis jitter')
    ax1.plot(time, V3jit + 0.1, label = 'V3 axis jitter')
    #ax1.plot(time, np.sqrt(V2jit**2 + V3jit**2), label = 'total jitter')
    ax1.set_xlabel('UT')
    ax1.set_ylabel('Jitter (arcsec)')
    ax1.legend(loc = 'best')
    ax1.set_ylim([-0.05, 0.15])
    plt.show()
    # df['jitter'] = AVGjit
    # df125 = df[df['FILTER'] == 'F125W']
    # df160 = df[df['FILTER'] == 'F160W']
    # ax1.plot(df125['jitter'], abs(df125['FLUX'] - df125['FLUX'].mean(axis = -1)), '+', label = 'F125W')
    # ax1.plot(df160['jitter'], abs(df160['FLUX'] - df160['FLUX'].mean(axis = -1)), 'x', label = 'F160W')
    # ax1.set_xlim([0, 0.2])
    # ax1.set_xlabel('RMS Jitter (arcsec)')
    # ax1.set_ylabel('Flux - Flux$_{avg}$')
    # plt.show()

    # # ax2 = ax1.twinx()
    # # ax2.plot(df[df['FILTER'] == 'F125W'].index, df[df['FILTER'] == 'F125W']['FLUX']/df[df['FILTER'] == 'F125W']['FLUX'].mean(axis = -1), '-.', label = 'F125W')
    # # ax2.plot(df[df['FILTER'] == 'F160W'].index, df[df['FILTER'] == 'F160W']['FLUX']/df[df['FILTER'] == 'F160W']['FLUX'].mean(axis = -1), '-+', label = 'F160W')
    # # ax2.set_xlabel('UT')
    # # ax2.set_ylabel('Relative Flux')
    # # ax2.legend(loc = 'best')

    # fig.autofmt_xdate()
    # plt.savefig('jitter.pdf')