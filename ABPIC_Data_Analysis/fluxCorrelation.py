#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd

if __name__ == '__main__':
    dataFile = sys.argv[1]
    target = sys.argv[2]
    df = pd.read_csv(dataFile)
    df['XC0'] = df['XCENTER'] - df['XOFF']
    df['YC0'] = df['YCENTER'] - df['YOFF']
    df['XMEAN'] = 0
    df['YMEAN'] = 0
    df.loc[(df['POSANG'] < 110) & (df['FILTER'] == 'F125W'), 'XMEAN'] = df[(df['POSANG']<110) & (df['FILTER'] == 'F125W')]['XC0'].mean()
    df.loc[(df['POSANG'] >= 110) & (df['FILTER'] == 'F125W'),'XMEAN'] = df[(df['POSANG']>=110) & (df['FILTER'] == 'F125W')]['XC0'].mean()
    df.loc[(df['POSANG'] < 110) & (df['FILTER'] == 'F125W'),  'YMEAN'] = df[(df['POSANG']<110) & (df['FILTER'] == 'F125W')]['YC0'].mean()
    df.loc[(df['POSANG'] >= 110) & (df['FILTER'] == 'F125W'), 'YMEAN'] = df[(df['POSANG']>=110) & (df['FILTER'] == 'F125W')]['YC0'].mean()
    
    df.loc[(df['POSANG'] < 110) & (df['FILTER'] == 'F160W'), 'XMEAN'] = df[(df['POSANG']<110) & (df['FILTER'] == 'F160W')]['XC0'].mean()
    df.loc[(df['POSANG'] >= 110) & (df['FILTER'] == 'F160W'),'XMEAN'] = df[(df['POSANG']>=110) & (df['FILTER'] == 'F160W')]['XC0'].mean()
    df.loc[(df['POSANG'] < 110) & (df['FILTER'] == 'F160W'),  'YMEAN'] = df[(df['POSANG']<110)& (df['FILTER'] == 'F160W')]['YC0'].mean()
    df.loc[(df['POSANG'] >= 110) & (df['FILTER'] == 'F160W'), 'YMEAN'] = df[(df['POSANG']>=110) & (df['FILTER'] == 'F160W')]['YC0'].mean()
    df['DELTA X'] = df['XC0'] - df['XMEAN']
    df['DELTA Y'] = df['YC0'] - df['YMEAN']
    df['FWHM'] = np.sqrt((df['XFWHM']**2 + df['YFWHM']**2)/2)
    
    subdf125 = df[df['FILTER'] == 'F125W']
    subdf160 = df[df['FILTER'] == 'F160W']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if target == 'x':
        ax.set_title('Flux vs x')
        ax.plot(subdf125['DELTA X'], subdf125['FLUX']/subdf125['FLUX'].mean(), '+', label = 'F125W')
        ax.plot(subdf160['DELTA X'], subdf160['FLUX']/subdf160['FLUX'].mean(), 'x', label = 'F160W')
        ax.set_xlabel('$\Delta x$')
        ax.set_ylabel('Normalized Flux')
                

    elif target == 'y':
        ax.set_title('Flux vs y')
        ax.plot(subdf125['DELTA Y'], subdf125['FLUX']/subdf125['FLUX'].mean(), '+', label = 'F125W')
        ax.plot(subdf160['DELTA Y'], subdf160['FLUX']/subdf160['FLUX'].mean(), 'x', label = 'F160W')
        ax.set_xlabel('$\Delta y$')
        ax.set_ylabel('Normalized Flux')

    elif target == 'dist':
        ax.set_title('Flux vs distance')
        ax.plot(np.sqrt((subdf125['YC0'] - subdf125['YMEAN'])**2 + (subdf125['XC0'] - subdf125['XMEAN'])**2), subdf125['FLUX']/subdf125['FLUX'].mean(), '+', label = 'F125W')
        ax.plot(np.sqrt((subdf160['YC0'] - subdf160['YMEAN'])**2 + (subdf160['XC0'] - subdf160['XMEAN'])**2), subdf160['FLUX']/subdf160['FLUX'].mean(), 'x', label = 'F160W')
        ax.set_xlabel('$\Delta$')
        ax.set_ylabel('Normalized Flux')
    elif target == 'FWHM':
        ax.set_title('Flux vs FWHM')
        ax.plot(subdf125['FWHM'], subdf125['FLUX']/subdf125['FLUX'].mean(), '+', label = 'F125W')
        ax.plot(subdf160['FWHM'], subdf160['FLUX']/subdf160['FLUX'].mean(), 'x', label = 'F160W')
        ax.set_xlabel('FWHM')
        ax.set_ylabel('Normalized Flux')

    elif target == 'XFWHM':
        ax.set_title('Flux vs XFWHM')
        ax.plot(subdf125['XFWHM'], subdf125['FLUX']/subdf125['FLUX'].mean(), '+', label = 'F125W')
        ax.plot(subdf160['XFWHM'], subdf160['FLUX']/subdf160['FLUX'].mean(), 'x', label = 'F160W')
        ax.set_xlabel('XFWHM')
        ax.set_ylabel('Normalized Flux')

    elif target == 'YFWHM':
        ax.set_title('Flux vs YFWHM')
        ax.plot(subdf125['YFWHM'], subdf125['FLUX']/subdf125['FLUX'].mean(), '+', label = 'F125W')
        ax.plot(subdf160['YFWHM'], subdf160['FLUX']/subdf160['FLUX'].mean(), 'x', label = 'F160W')
        ax.set_xlabel('YFWHM')
        ax.set_ylabel('Normalized Flux')

    elif target == 'sky':
        ax.set_title('Flux vs Sky')
        ax.plot(subdf125['SKY_LEVEL'], subdf125['FLUX']/subdf125['FLUX'].mean(), '+', label = 'F125W')
        ax.plot(subdf160['SKY_LEVEL'], subdf160['FLUX']/subdf160['FLUX'].mean(), 'x', label = 'F160W')
        ax.set_xlabel('SKY_LEVEL')
        ax.set_ylabel('Normalized Flux')
    else:
        pass

    plt.show()
                