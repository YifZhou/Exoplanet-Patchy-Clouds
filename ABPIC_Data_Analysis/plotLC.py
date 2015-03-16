import matplotlib.pyplot as plt
import pandas as pd
import sys

if __name__ == '__main__':
    fn = sys.argv[1]
    df = pd.read_csv(fn, parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    plt.close('all')
    plt.plot(df[df['FILTER'] == 'F125W'].index, df[df['FILTER'] == 'F125W']['FLUX']/df[df['FILTER'] == 'F125W']['FLUX'].mean(), '+')
    plt.plot(df[df['FILTER'] == 'F160W'].index, df[df['FILTER'] == 'F160W']['FLUX']/df[df['FILTER'] == 'F160W']['FLUX'].mean() + 0.05, 'x')
    plt.gcf().autofmt_xdate()
    plt.show()