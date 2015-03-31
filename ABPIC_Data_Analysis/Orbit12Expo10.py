#! /usr/bin/env python
import sys
sys.path.append('../python_src')
from CCD import CCD
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    size = 11
    nSamp = 50
    wfc3 = CCD(size, nSamp, 0.1, fluctuate = 0.1)
    df = pd.read_csv('jitter_info.csv', parse_dates = 'time', index_col = 'time')
    