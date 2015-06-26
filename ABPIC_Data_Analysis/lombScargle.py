import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import lombscargle  # lomb scargle method
import sys
import numpy as np

if __name__ == '__main__':
    df = pd.read_csv(sys.argv[1], parse_dates={
                     'datetime': ['OBS_DATE', 'OBS_TIME']}, index_col='datetime')
    df125 = df[df['FILTER'] == 'F125W']
    df125['Normed Flux'] = np.zeros(len(df125))
    for orbit in [10, 11, 12]:
        df125.loc[df125['ORBIT'] == orbit, 'Normed Flux'] = df125[
            df125['ORBIT'] == orbit]['FLUX'] / df125[df125['ORBIT'] == orbit]['FLUX'].mean()

    # t in min
    t = (df125.index.values -
         df125.index.values[0]).astype(float) / (60. * 1e9)
    nflux = df125['Normed Flux'].values

    freq = np.linspace(0.001, 5, 10000)
    pgram = lombscargle(t, nflux, freq)
    plt.plot(freq, pgram)
    plt.show()
