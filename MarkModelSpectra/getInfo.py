#! /usr/bin/env python
from __future__ import print_function, division
from glob import glob
import re
import pandas as pd
import numpy as np
"""generate file info
"""

if __name__ == '__main__':
    info = pd.DataFrame()
    fileList = glob('*.flx')
    fileList.sort()
    info['file name'] = fileList
    T = np.zeros(len(fileList), dtype=int)
    g = np.zeros(len(fileList), dtype=int)
    fsed = np.zeros(len(fileList), dtype=int)
    TPattern = re.compile(r't[0-9]{3,4}')
    gPattern = re.compile(r'g[0-9]{3,4}')
    fsedPattern = re.compile(r'f[0-9]\.')
    for i, fn in enumerate(fileList):
        T[i] = int(TPattern.search(fn).group()[1:])
        g[i] = int(gPattern.search(fn).group()[1:])
        fsed[i] = int(fsedPattern.search(fn).group()[1])
    info['T'] = T
    info['g'] = g
    info['fsed'] = fsed
    info.to_csv('Marley_Model_info.csv', index=False)
