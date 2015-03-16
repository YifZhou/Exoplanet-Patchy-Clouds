from astropy.io import fits
import numpy as np
import glob
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def getJitInfo(outfn = None):
    dataDIR = '../data/ABPIC-B/'
    jitFileList = glob.glob(dataDIR + '*jit.fits')
    jitFileList.sort()
    time = []
    JitV2 = []
    JitV3 = []
    domV2 = []
    domV3 = []
    rollV2 = []
    rollV3 = []
    RA = []
    DEC = []
    Roll = []
    orbit = []
    filenames = []
    filters = []
    for fn in jitFileList:
        nExt = fits.getheader(fn, 0)['NEXTEND'] #get the number of extensions
        if nExt == 5:
            filtername = 'F160W'
        elif nExt == 4:
            filtername = 'F125W'
        for iExt in range(1, 1 + nExt):
            data, hd = fits.getdata(fn, 'jit', iExt, header = True)
            expName = hd['expname'][0:-1] + 'q' #flt file and jit file have different indicator for the last letter
            obsDate = fits.getheader(dataDIR + expName + '_flt.fits', extname = 'primary')['date-obs']
            obsTime = fits.getheader(dataDIR + expName + '_flt.fits', extname = 'primary')['time-obs']
            startTime = np.datetime64('T'.join([obsDate, obsTime]))
            time += (startTime + (data['seconds']*1e3).astype('timedelta64[ms]')).tolist() # to ms precison
            JitV2 += data['SI_V2_AVG'].tolist()
            JitV3 += data['SI_V3_AVG'].tolist()
            domV2 += data['V2_dom'].tolist()
            domV3 += data['V3_dom'].tolist()
            rollV2 += data['V2_roll'].tolist()
            rollV3 += data['V3_roll'].tolist()
            RA += data['RA'].tolist()
            DEC += data['DEC'].tolist()
            Roll += data['Roll'].tolist()
            orbit += [int(hd['obset_ID'])] * len(data)
            filenames += [expName] * len(data)
            filters += [filtername] * len(data)

    df = pd.DataFrame()
    df['file name'] = filenames
    df['orbit'] = orbit
    df['filter'] = filters
    df['time'] = time
    df['dom V2'] = domV2
    df['dom V3'] = domV3
    df['roll V2'] = rollV2
    df['roll V3'] = rollV3
    df['jitter V2'] = JitV2
    df['jitter V3'] = JitV3
    df['RA'] = RA
    df['DEC'] = DEC
    df['roll'] = Roll
    df.loc[(df['jitter V2'].abs() > 10), 'jitter V2'] = np.nan
    df.loc[(df['jitter V3'].abs() > 10), 'jitter V3'] = np.nan
    df.loc[(df['RA'].abs() > 1e5), 'RA'] = np.nan
    df.loc[(df['DEC'].abs() > 1e5), 'DEC'] = np.nan
    if outfn is not None:
        df.to_csv(outfn,index = False)
        return 0
    else:
        return df

def plotJitter(df, orbit, filterName, save = False):
    """
    plot the Jitter track
    """
    plt.close('all')
    fig = plt.figure(figsize = (12, 6))
    ax = fig.add_subplot(121)
    subdf = df[(df['orbit'] == orbit) & (df['filter'] == filterName)]
    V2 = (subdf['jitter V2']).values
    V3 = (subdf['jitter V3']).values
    time = (subdf.index.values - subdf.index.values[0])/1.e9 #in seconds
    ax.plot(V2/0.13, V3/0.13, color = '0.7', linewidth = 0.6)
    ax.scatter(V2[::-1]/0.13, V3[::-1]/0.13, c = time[::-1], marker = '.', s = 50, cmap = 'gray', zorder = 5, lw = 1)
    ax.set_xlabel('V2 Jitter (pixel)')
    ax.set_ylabel('V3 Jitter (pixel)')
    ax.set_xlim([-0.1, 0.1])
    ax.set_ylim([-0.1, 0.1])
    ax.set_aspect('equal')


    axV2 = fig.add_subplot(222)
    axV2.plot(time, V2/0.13)
    axV2.set_xlabel('time (s)')
    axV2.set_ylabel('Jitter (pixel)')
    axV2.set_title('V2 Jitter')

    axV3 = fig.add_subplot(224, sharex = axV2)
    axV3.plot(time, V3/0.13)
    axV3.set_xlabel('time (s)')
    axV3.set_ylabel('Jitter (pixel)')
    axV3.set_title('V3 Jitter')
    fig.suptitle('Orbit: {0}, Filter: {1}'.format(orbit, filterName))
    fig.tight_layout()
    if not save:
        plt.show()
    else:
        plt.savefig('JitterTrack_{0}_{1}.pdf'.format(orbit, filterName))


        
if __name__ == '__main__':
    #getJitInfo('jitter_info.csv')
    df = pd.read_csv('jitter_info.csv', parse_dates = 'time', index_col = 'time')
    plotJitter(df, 10, 'F125W')