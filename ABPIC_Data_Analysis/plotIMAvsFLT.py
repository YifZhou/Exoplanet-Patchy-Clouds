import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if __name__ == '__main__':
    ima = pd.read_csv('2015_Feb_10_ima_aper=5_result.csv', parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    flt = pd.read_csv('2015_Feb_10_flt_aper=5_result.csv', parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    fluxRatio = ima['FLUX']/flt['FLUX']
    print ima[np.abs(fluxRatio - 1) > 0.02]['FILENAME']
    plt.close('all')
    plt.plot(ima.index, fluxRatio)
    plt.show()