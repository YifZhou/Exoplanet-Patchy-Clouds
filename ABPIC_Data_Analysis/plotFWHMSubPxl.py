#! /usr/bin/env python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    #fn = 'Jan_07_F125W_result.csv'
    fn = '2015_Jan_07_result.csv'
    DF = pd.read_csv(fn)
    fig = plt.figure(figsize = (12,6))
    ax_125 = fig.add_subplot(121)
    ax_160 = fig.add_subplot(122)
    DF125 = DF[DF['FILTER'] == 'F125W']
    DF160 = DF[DF['FILTER'] == 'F160W']
    print len(DF160)
    ax_125.plot(np.abs(DF125['XCENTER'] - np.around(DF125['XCENTER'])), DF125['XFWHM'], lw = 0, marker = 'x')
    ax_125.plot(np.abs(DF125['YCENTER'] - np.around(DF125['YCENTER'])), DF125['YFWHM'], lw = 0, marker = '3')
    ax_125.set_xlabel('$\Delta$ (pixels)')
    ax_125.set_ylabel('FWHM')
    ax_125.set_title('F125W')

    ax_160.plot(np.abs(DF160['XCENTER'] - np.around(DF160['XCENTER'])), DF160['XFWHM'], lw = 0, marker = 'x')
    ax_160.plot(np.abs(DF160['YCENTER'] - np.around(DF160['YCENTER'])), DF160['YFWHM'], lw = 0, marker = '3')
    ax_160.set_xlabel('$\Delta$ (pixels)')
    ax_160.set_ylabel('FWHM')
    ax_160.set_title('F160W')

    fig.tight_layout()

    plt.savefig('fwhm_vs_subpixel.pdf')
            
            
            