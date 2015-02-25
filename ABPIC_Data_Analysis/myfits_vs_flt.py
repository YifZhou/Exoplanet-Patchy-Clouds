import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    fltdf = pd.read_csv('2015_Feb_10_flt_aper=5_result.csv', parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    mydf = pd.read_csv('2015_Feb_23_myfits_aper=5_result.csv', parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')

    fltdf = fltdf[fltdf['ORBIT']>=10]
    fig = plt.figure(figsize = (8,6))
    ax125 = fig.add_subplot(211)
    ax125.set_title('F125W')
    ax160 = fig.add_subplot(212)
    ax160.set_title('F160W')

    for ax, band, expt in zip([ax125, ax160], ['F125W', 'F160W'], [30., 15.]):
        ax.errorbar(fltdf[fltdf['FILTER'] == band].index, fltdf[fltdf['FILTER'] == band]['FLUX'], yerr = np.sqrt(fltdf[fltdf['FILTER'] == band]['FLUX'])/np.sqrt(expt), fmt = 'o', label = 'flt')
        ax.errorbar(mydf[mydf['FILTER'] == band].index, mydf[mydf['FILTER'] == band]['FLUX'], yerr = np.sqrt(mydf[fltdf['FILTER'] == band]['FLUX'])/np.sqrt(expt), fmt = 's', label = 'corrected')

    for ax in [ax125, ax160]:
        ax.set_xlabel('UT')
        ax.set_ylabel('flux (e$^-$/s)')

    fig.autofmt_xdate()
    plt.show()
