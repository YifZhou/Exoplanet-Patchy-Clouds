#! /usr/bin/env python
from scipy.io.idl import readsav
import sys
import pandas as pd

if __name__ == '__main__':
    infn = sys.argv[1]
    outfn = sys.argv[2]
    df = pd.DataFrame()
    data = readsav(infn)
    strct = data.infoStruct1
    for key in strct.dtype.names:
        df[key] = strct[key][0]

    df.to_csv(outfn, index = False)

