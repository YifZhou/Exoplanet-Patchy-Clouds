from PSF_generator import exposureFocus
import pandas as pd
from astropy.io import fits
import numpy as np

if __name__ == '__main__':
    fn125 = '2015_Jun_24TinyTimF125Result.csv'
    fn160 = '2015_Jun_24TinyTimF160Result.csv'
    df125 = pd.read_csv(
        fn125, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    df160 = pd.read_csv(
        fn160, parse_dates={'datetime': ['OBSDATE', 'OBSTIME']},
        index_col='datetime')
    filePath = '../data/2M1207B/'
    fn = df125['FILENAME'].values
    focus = np.zeros(len(fn))
    for i, fn in enumerate(fn):
        hd = fits.getheader(filePath + fn, 0)
        MJD = hd['EXPSTART']
        focus[i] = exposureFocus(MJD)
    df125['focus'] = pd.Series(focus, index=df125.index)
