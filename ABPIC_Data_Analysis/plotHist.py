#/usr/bin/env python
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
plt.style.use('ggplot')

def normalize(df):
    """
    normalize the flux by filter and angle
    """
    
    flux0 = np.zeros(len(df))
    flux0[np.where((df['FILTER'] == 'F125W') & (df['POSANG'] == 129))] = df[(df['FILTER'] == 'F125W') & (df['POSANG'] == 129)]['FLUX']/df[(df['FILTER'] == 'F125W') & (df['POSANG'] == 129)]['FLUX'].mean()
    flux0[np.where((df['FILTER'] == 'F125W') & (df['POSANG'] == 101))] = df[(df['FILTER'] == 'F125W') & (df['POSANG'] == 101)]['FLUX']/df[(df['FILTER'] == 'F125W') & (df['POSANG'] == 101)]['FLUX'].mean()
    flux0[np.where((df['FILTER'] == 'F160W') & (df['POSANG'] == 129))] = df[(df['FILTER'] == 'F160W') & (df['POSANG'] == 129)]['FLUX']/df[(df['FILTER'] == 'F160W') & (df['POSANG'] == 129)]['FLUX'].mean()
    flux0[np.where((df['FILTER'] == 'F160W') & (df['POSANG'] == 101))] = df[(df['FILTER'] == 'F160W') & (df['POSANG'] == 101)]['FLUX']/df[(df['FILTER'] == 'F160W') & (df['POSANG'] == 101)]['FLUX'].mean()
    return flux0
    
if __name__ == '__main__':
    fltFN = '2015_Feb_10_flt_aper=5_result.csv'
    newFN = '2015_May_02_noramp_aper=5.00_result.csv'
    fltDF = pd.read_csv(fltFN, parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    newDF = pd.read_csv(newFN, parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    fltDF = fltDF[fltDF['ORBIT']>=10]
    newDF = newDF[newDF['ORBIT']>=10]
    cosmicRayDF = pd.read_csv('totalRampUp_size_7_result.csv', parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    fltDF['FLUX'][np.where(np.isnan(cosmicRayDF['FLUX']))[0]] = np.nan
    newDF['FLUX'][np.where(np.isnan(cosmicRayDF['FLUX']))[0]] = np.nan
    plt.close('all')
    fig1, ax1 = plt.subplots()
    fltFlux0 = normalize(fltDF)
    newFlux0 = normalize(newDF)
    ax1.hist(fltFlux0[np.where(fltDF['FILTER'] == 'F125W')], bins = np.linspace(0.98, 1.02, 12), alpha = 0.8, label = 'flt, std = {0:.2f}%'.format(np.nanstd(fltFlux0[np.where(fltDF['FILTER'] == 'F125W')])*100))
    ax1.hist(newFlux0[np.where(newDF['FILTER'] == 'F125W')], bins = np.linspace(0.98, 1.02, 12), alpha = 0.8, label = 'corrected, std = {0:.2f}%'.format(np.nanstd(newFlux0[np.where(newDF['FILTER'] == 'F125W')])*100))
    ax1.set_xlabel('Normalized flux')
    ax1.set_ylabel('N exposures')
    ax1.set_title('F125W')
    ax1.legend(loc = 'best')

    fig2, ax2 = plt.subplots()
    ax2.hist(fltFlux0[np.where(fltDF['FILTER'] == 'F160W')], bins = np.linspace(0.98, 1.02, 12), alpha = 0.8, label = 'flt, std = {0:.2f}%'.format(np.nanstd(fltFlux0[np.where(fltDF['FILTER'] == 'F160W')])*100))
    ax2.hist(newFlux0[np.where(newDF['FILTER'] == 'F160W')], bins = np.linspace(0.98, 1.02, 12), alpha = 0.8, label = 'corrected, std = {0:.2f}%'.format(np.nanstd(newFlux0[np.where(newDF['FILTER'] == 'F160W')])*100))
    ax2.set_xlabel('Normalized flux')
    ax2.set_ylabel('N exposures')
    ax2.set_title('F160W')
    ax2.legend(loc = 'best')
    fig1.savefig('F125W_hist.pdf')
    fig2.savefig('F160W_hist.pdf')
    
    