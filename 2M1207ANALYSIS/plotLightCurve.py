#! /usr/bin/env python
from __future__ import print_function
import matplotlib.pyplot as plt
import pandas as pd
from linearFit import linearFit
import numpy as np
plt.style.use('ggplot')

def plotLightCurve(DataFrame125, DataFrame160, doCorrection = False):
    """
    
    Arguments:
    - `DataFrame125`: Data Frame for F125W
    - `DataFrame160`: Data Frame for F160W
    - `doCorrection`: if correct the flux of secondary using the flux of primary
    
    read the data frame and plot the light curve,
    The flux for secondary is seemed to be anti-correlated with the flux for primary, decide if do the correction
    """
    fig = plt.figure(figsize = (12, 6))
    ax_F125 = fig.add_subplot(121)
    ax_F160 = fig.add_subplot(122)
    ax_F125.plot(DataFrame125.index, DataFrame125['FLUXA']/DataFrame125['FLUXA'].mean(), linewidth = 0, marker = 's', label = 'priamry')
    ax_F125.plot(DataFrame125.index, DataFrame125['FLUXB']/DataFrame125['FLUXB'].mean(), linewidth = 0, marker = 'o', label = 'secondary')
    ax_F125.set_title('F125W')
    ax_F160.plot(DataFrame160.index, DataFrame160['FLUXA']/DataFrame160['FLUXA'].mean(), linewidth = 0, marker = 's', label = 'primary')
    ax_F160.plot(DataFrame160.index, DataFrame160['FLUXB']/DataFrame160['FLUXB'].mean(), linewidth = 0, marker = 'o', label = 'secondary')
    ax_F160.set_title('F160W')
    
    for ax in fig.get_axes():
        ax.set_xlabel('Time')
        ax.set_ylabel('Normalized flux')
        #ax.legend(loc='best')
    fig.autofmt_xdate()
    return fig

def correlation(df, ifPlot = True):
    """
    
    Arguments:
    - `df`: dataframe
    - `ifPlot`: if make the plot
    """
    x = df['FLUXA']/df['FLUXA'].mean()
    y = df['FLUXB']/df['FLUXB'].mean()
    fitResult = linearFit(x, y)
    if ifPlot:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x, y, linewidth = 0, marker = 'o')
        xx = np.linspace(x.min(), x.max(), 100)
        ax.plot(xx, xx*fitResult[1] + fitResult[0])
        return fig
    
        
if __name__ == '__main__':
    fn125 = 'TinyTimF125Result.csv'
    fn160 = 'TinyTimF160Result.csv'
    df125 = pd.read_csv(fn125, parse_dates = {'datetime':['OBSDATE', 'OBSTIME']}, index_col = 'datetime')
    df160 = pd.read_csv(fn160, parse_dates = {'datetime':['OBSDATE', 'OBSTIME']}, index_col = 'datetime')
    fig1 = plotLightCurve(df125, df160)
    fig2 = correlation(df125)
    plt.show()



    
