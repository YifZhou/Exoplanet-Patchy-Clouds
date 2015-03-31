import matplotlib.pyplot as plt
import pickle
import glob

def plotTrend (HSTFile, side = 2, output = None):#2side+1 x 2side+1 pixels subimage
    plt.close('all')
    fig, axes = plt.subplots(ncols = 2*side + 1, nrows = 2*side + 1, sharex = True, sharey = True, figsize = (24, 20))
    fig.subplots_adjust(hspace = 0, wspace = 0)
    size = HSTFile.countArray.shape[0]
    c = size//2
    for i, dim0 in enumerate(range(c-side, c+side+1)):
        for j, dim1 in enumerate(range(c-side, c+side+1)):
            fitList = HSTFile.fitCountArray[dim0, dim1] * HSTFile.expTime + HSTFile.zeroValue[dim0, dim1]
            countList = HSTFile.countArray[dim0, dim1, :]
            axes[i, j].plot(HSTFile.expTime, countList/fitList, linewidth = 0, marker = '.')
            axes[i, j].axhline(y = 1.0)
            axes[i, j].annotate('x={0},y={1}'.format(dim1 - c, dim0 - c), xy = (0.2, 0.8), xycoords = 'axes fraction')
            axes[i, j].xaxis.set_major_locator(plt.MaxNLocator(4))
            axes[i, j].set_ylim([0.8, 1.2])

    if output is None:
        plt.show()
    else:
        plt.savefig(output)

if __name__ == '__main__':
    pklList = glob.glob('../data/ABPIC-B_myfits/icdg*pkl')
    pklList.sort()
    for fn in pklList:
        hst = pickle.load(open(fn, 'rb'))
        outputFN = fn.split('/')[-1].rstrip('.pkl')
        plotTrend(hst, output = './JitterRamp/{0}.pdf'.format(outputFN))