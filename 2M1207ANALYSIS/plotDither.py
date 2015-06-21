#! /usr/bin/env python
from __future__ import print_function, division
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

"""plot flux as a function of dither position
"""
plt.style.use('myggplot')

markers = ['_', '+', '^', 's', 'p', 'h']
colors = mpl.rcParams['axes.color_cycle']


def plotDither(df):
    """the function to do this
    """
    df['FLUXA0'] = df['FLUXA'] / df['FLUXA'].mean()
    df['FLUXB0'] = df['FLUXB'] / df['FLUXB'].mean()
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212, sharex=ax1)
    for angle in [0, 1]:
        for dither in range(4):
            pos = angle * 4 + dither
            subdf = df[(df['POSANGLE'] == angle) & (df['DITHER'] == dither)]
            for orbit in range(6):
                ax1.plot([pos] * len(subdf[subdf['ORBIT'] == orbit + 1]),
                         subdf[subdf['ORBIT'] == orbit + 1]['FLUXA0'],
                         linewidth=0, marker=markers[orbit],
                         ms=8, mew=2, mec=colors[orbit],
                         color=colors[orbit], alpha=0.8)
                ax2.plot([pos] * len(subdf[subdf['ORBIT'] == orbit + 1]),
                         subdf[subdf['ORBIT'] == orbit + 1]['FLUXB0'],
                         linewidth=0, marker=markers[orbit],
                         ms=8, mew=2, mec=colors[orbit],
                         color=colors[orbit], alpha=0.8)

            ax1.errorbar(pos + 0.1, subdf['FLUXA0'].mean(),
                         yerr=subdf['FLUXA0'].std(),
                         fmt='o', color='k', elinewidth=2.5, zorder=5)
            ax2.errorbar(pos + 0.1, subdf['FLUXB0'].mean(),
                         yerr=subdf['FLUXB0'].std(),
                         fmt='o', color='k', elinewidth=2.5, zorder=5)

    for ax in [ax1, ax2]:
        ax.set_xlabel('Position')

    ax1.set_ylabel('Primary Flux')
    ax2.set_ylabel('Secondary Flux')
    return fig


if __name__ == '__main__':
    plt.close('all')
    df125 = pd.read_csv('2015_Jun_17TinyTimF125Result.csv', parse_dates={
                        'datetime': ['OBSDATE', 'OBSTIME']},
                        index_col='datetime')
    fig1 = plotDither(df125)
    fig1.suptitle('F125W')
    df160 = pd.read_csv('2015_Jun_17TinyTimF160Result.csv', parse_dates={
                        'datetime': ['OBSDATE', 'OBSTIME']},
                        index_col='datetime')
    fig2 = plotDither(df160)
    fig2.suptitle("F160W")
    for fig in [fig1, fig2]:
        fig.tight_layout()
    plt.show()
