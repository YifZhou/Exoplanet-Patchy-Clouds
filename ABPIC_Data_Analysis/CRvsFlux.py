#! /usr/bin/env python
"""
investigate how CR affect _ima to _flt conversion
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    fltDF = pd.read_csv('2015_Jan_07_result.csv', parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    imaDF = pd.read_csv('ima_DataQuality.csv', parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    plt.close('all')
    fig = plt.figure()
    Diff = imaDF['FLUX']-fltDF['FLUX']
    ax = fig.add_subplot(111)
    ax.plot(imaDF['CR number'], np.abs(Diff), '.')
    plt.show()

