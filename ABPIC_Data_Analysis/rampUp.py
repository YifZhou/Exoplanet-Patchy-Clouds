from astropy.io import fits
import matplotlib.pyplot as plt
import sys
import os
import numpy as np

if __name__ == '__main__':
    dataDIR = '../data/ABPIC-B'
    fn = sys.argv[1]
    x = int(sys.argv[2]) 
    y = int(sys.argv[3]) # do not use x or y, they are confusing
    dim1, dim2 = y, x
    ima = fits.open(os.path.join(dataDIR, fn))
    nSamp = ima['primary'].header['nsamp']
    count = np.zeros(nSamp)
    sampTime = np.zeros(nSamp)
    count[0] = ima['sci', nSamp].data[dim1, dim2]
    sampTime[0] = 0 # zeroth read
    for i, samp_i in enumerate(range(nSamp - 1, 0, -1)): #last samp is the first readout
        sampTime[i+1] = ima['sci', samp_i].header['samptime']
        print ima['sci', samp_i].data[dim1, dim2], ima['dq', samp_i].data[dim1, dim2]
        count[i+1] = ima['sci', samp_i].data[dim1, dim2] * sampTime[i + 1] + count[0]

    plt.close('all')
    plt.plot(sampTime, count, marker = '+')
    print sampTime, count
    ax = plt.gca()
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Count (e$^-$)')
    plt.show()

    