#! /usr/bin/env python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    #fn = 'Jan_07_F125W_result.csv'
    fn = 'Jan_07_F125W_result.csv'
    DF = pd.read_csv(fn)
    fig = plt.figure(figsize = (6,12))
    ax_x = fig.add_subplot(311)
    ax_y = fig.add_subplot(312, sharex = ax_x)
    ax_xy = fig.add_subplot(313, sharex = ax_x)
    pos = 0
    for angle in [101, 129]:
        for dither in range(4):
            pos += 1
            subDF = DF[(DF['POSANG'] == angle) & (DF['DITHER'] == dither)]
            print angle, dither, len(subDF)
            ax_x.plot(np.abs(subDF['XCENTER'] - np.around(subDF['XCENTER'])), subDF['FLUX'], lw = 0, marker = '${0}$'.format(pos))
            ax_x.set_xlabel('X (pixels)')
            ax_x.set_ylabel('Flux')
            ax_y.plot(np.abs(subDF['YCENTER'] - np.around(subDF['YCENTER'])), subDF['FLUX'], lw = 0, marker = '${0}$'.format(pos))
            ax_y.set_xlabel('Y (pixels)')
            ax_y.set_ylabel('Flux')
            ax_xy.plot(np.sqrt((subDF['XCENTER'] - np.around(subDF['XCENTER']))**2 + 
                               (subDF['YCENTER'] - np.around(subDF['YCENTER']))**2), subDF['FLUX'], lw = 0, marker = '${0}$'.format(pos))
            ax_xy.set_xlabel('$\sqrt{x^2+y^2}$ (pixel)')
            ax_xy.set_ylabel('Flux')

    fig.suptitle('F125W')            
    fig.tight_layout()


    plt.savefig('F125W_flux_vs_subpixel.pdf')
            
            
            