#! /usr/bin/env python
from scipy.io.idl import readsav
import sys
import pandas as pd

if __name__ == '__main__':
    infn = sys.argv[1]
    saveVar = sys.argv[2]
    outfn = sys.argv[3]
    df = pd.DataFrame()
    data = readsav(infn)
    exec('strct = data.' + saveVar)
    for key in strct.dtype.names:
        df[key] = strct[key][0]

    df.to_csv(outfn, index = False)

