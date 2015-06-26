#! /usr/bin/env python
from __future__ import print_function
import matplotlib.pyplot as plt
import pandas as pd
from linearFit import linearFit
import numpy as np
plt.style.use('myggplot')


def normFlux(dataFrame, normDither=False):
    """    Keyword Arguments:
    dataFrame  -- input data frame
    normDither -- (default False) if normalize by dither position, default
    is faulse
    reurn the normalized flux for primary and secondary
    """
    fluxA0 = np.zeros(len(dataFrame))
    fluxB0 = np.zeros(len(dataFrame))
    if normDither:
        for angle in [0, 1]:
            for dither in range(4):
                subDF_id = np.where((dataFrame['POSANGLE'] == angle) &
                                    (dataFrame['DITHER'] == dither))
                subDF = dataFrame[(dataFrame['POSANGLE'] == angle) &
                                  (dataFrame['DITHER'] == dither)]
                fluxA0[subDF_id] = subDF['FLUXA'] / subDF['FLUXA'].mean()
                fluxB0[subDF_id] = subDF['FLUXB'] / subDF['FLUXB'].mean()
    if not normDither:
        fluxA0 = dataFrame['FLUXA'] / dataFrame['FLUXA'].mean()
        fluxB0 = dataFrame['FLUXB'] / dataFrame['FLUXB'].mean()

    return fluxA0, fluxB0


def plotLightCurve(DataFrame125, DataFrame160, doCorrection=False):
    """

    Arguments:
    - `DataFrame125`: Data Frame for F125W
    - `DataFrame160`: Data Frame for F160W
    - `doCorrection`: if correct the flux of secondary
    using the flux of primary

    read the data frame and plot the light curve,
    The flux for secondary is seemed to be anti-correlated with
    the flux for primary, decide if do the correction
    """
    fig = plt.figure(figsize=(12, 6))
    ax_F125 = fig.add_subplot(121)
    ax_F160 = fig.add_subplot(122, sharey=ax_F125)
    fluxA1250, fluxB1250 = normFlux(DataFrame125, normDither=True)
    fluxA1600, fluxB1600 = normFlux(DataFrame160, normDither=True)
    ax_F125.plot(DataFrame125.index, fluxA1250,
                 linewidth=0, marker='s', label='priamry')
    ax_F125.plot(DataFrame125.index, fluxB1250,
                 linewidth=0, marker='o', label='secondary')
    ax_F125.set_title('F125W')
    ax_F160.plot(DataFrame160.index, fluxA1600,
                 linewidth=0, marker='s', label='primary')
    ax_F160.plot(DataFrame160.index, fluxB1600,
                 linewidth=0, marker='o', label='secondary')
    ax_F160.set_title('F160W')
    # fluxA1250 = (DataFrame125['FLUXA'] / DataFrame125['FLUXA'].mean()).values
    # fluxA1600 = (DataFrame160['FLUXA'] / DataFrame160['FLUXA'].mean()).values
    print('Peak to Peak difference for primary:')
    print('F125W {0:.4f}'.format(fluxA1250.max() - fluxA1250.min()))
    print('F160W {0:.4f}'.format(fluxA1600.max() - fluxA1600.min()))
    print('Standard Deviation for primary:')
    print('F125W {0:.4f}'.format(fluxA1250.std()))
    print('F160W {0:.4f}'.format(fluxA1600.std()))
    for ax in fig.get_axes():
        ax.set_xlabel('Time')
        ax.set_ylabel('Normalized flux')
        ax.legend(loc='best')
        xlim = ax.get_xlim()
        dx = (xlim[1] - xlim[0]) * 0.1
        ax.set_xlim([xlim[0] - dx, xlim[1] + dx])
    fig.autofmt_xdate()
    return fig


def correlation(df, ifPlot=True):
    """

    Arguments:
    - `df`: dataframe
    - `ifPlot`: if make the plot
    """
    x = df['FLUXA'] / df['FLUXA'].mean()
    y = df['FLUXB'] / df['FLUXB'].mean()
    fitResult = linearFit(x.values, y.values)
    if ifPlot:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x, y, linewidth=0, marker='o')
        xx = np.linspace(x.min(), x.max(), 100)
        ax.plot(xx, xx * fitResult[1] + fitResult[0])
        ax.set_xlabel('Primary')
        ax.set_ylabel('Secondary')
        return fig


if __name__ == '__main__':
    fn125 = '2015_Jun_24TinyTimF125Result.csv'
    fn160 = '2015_Jun_24TinyTimF160Result.csv'
    df125 = pd.read_csv(
        fn125, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    df160 = pd.read_csv(
        fn160, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    fig1 = plotLightCurve(df125, df160)
    fig2 = correlation(df125)
    fig3 = correlation(df160)
    plt.show()
