#! /usr/bin/env python
from __future__ import print_function, division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
"""plot the histgram of chisq distribution of the fit
"""

if __name__ == '__main__':
    fn125 = '2015_Jun_24TinyTimF125Result.csv'
    fn160 = '2015_Jun_24TinyTimF160Result.csv'
    df125 = pd.read_csv(
        fn125, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime').sort_index()
    df160 = pd.read_csv(
        fn160, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime').sort_index()
    chisq = np.concatenate([df125['CHISQ'].values, df160['CHISQ'].values])
    fig1 = plt.figure()
    bins = np.linspace(chisq.min(), chisq.max(), 15)
    ax1 = fig1.add_subplot(111)
    ax1.hist(df125['CHISQ'].values, bins=bins)
    ax1.set_title('F125W')
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.hist(df160['CHISQ'].values, bins=bins)
    ax2.set_title('F160W')

    fig3 = plt.figure()
    ax3 = fig3.add_subplot(111)
    ax3.hist(chisq, bins=bins)
    for ax in [ax1, ax2, ax3]:
        ax.set_xlabel('Reduced $\chi^2$')
        ax.set_ylabel('Count')

    fig1.savefig('F125W_chsiq_dist.pdf')
    fig2.savefig('F160W_chisq_dist.pdf')
    fig3.savefig('chisq_dist.png', dpi=300)
