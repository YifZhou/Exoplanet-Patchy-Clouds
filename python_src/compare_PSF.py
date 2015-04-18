from astropy.io import fits
import matplotlib.pyplot as plt
from scipy import optimize
import numpy as np
import sys
"""
2d gaussian fit
"""
def gaussian(height, center_x, center_y, width_x, width_y):
    """Returns a gaussian function with the given parameters"""
    width_x = float(width_x)
    width_y = float(width_y)
    return lambda x,y: height*np.exp(
                -(((center_x-x)/width_x)**2+((center_y-y)/width_y)**2)/2)

def moments(data):
    """Returns (height, x, y, width_x, width_y)
    the gaussian parameters of a 2D distribution by calculating its
    moments """
    total = data.sum()
    X, Y = np.indices(data.shape)
    x = (X*data).sum()/total
    y = (Y*data).sum()/total
    col = data[:, int(y)]
    width_x = np.sqrt(np.abs((np.arange(col.size)-y)**2*col).sum()/col.sum())
    row = data[int(x), :]
    width_y = np.sqrt(np.abs((np.arange(row.size)-x)**2*row).sum()/row.sum())
    height = data.max()
    return height, x, y, width_x, width_y

def fitgaussian(data):
    """Returns (height, x, y, width_x, width_y)
    the gaussian parameters of a 2D distribution found by a fit"""
    params = moments(data)
    errorfunction = lambda p: np.ravel(gaussian(*p)(*np.indices(data.shape)) -
                                 data)
    p, success = optimize.leastsq(errorfunction, params)
    return p

def compare_PSF(image1, image2, center1, center2, ncol = 5):
    sub1 = image1[round(center1[1])-5:round(center1[1])+6,
                  round(center1[0])-5:round(center1[0])+6]
    sub2 = image2[round(center2[1])-5:round(center2[1])+6,
                  round(center2[0])-5:round(center2[0])+6]
    center1 = fitgaussian(sub1)[1:3]
    center2 = fitgaussian(sub2)[1:3]
    plt.close('all')
    fig = plt.figure()
    x0 = np.arange(11)
    for i in range(ncol):
        ax1 = fig.add_subplot(2, 5, i)
        ax2 = fig.add_subplot(2, 5, i+5)
        ax1.plot(x0 - center1[1] + 5, sub1[2+i,:], linestyle = 'steps', color = 'b')
        ax1.plot(x0 - center2[1] + 5, sub2[2+i,:], linestyle = 'steps', color = 'r')
        ax2.plot(x0 - center1[0] + 5, sub1[:,2+i], linestyle = 'steps', color = 'b')
        ax2.plot(x0 - center2[0] + 5, sub2[:,2+i], linestyle = 'steps', color = 'r')
    fig.tight_layout()
    plt.show()
    
if __name__ == '__main__':
    fn1 = '../data/ABPIC-B_noramp/icdg08r0q_noramp.fits'
    fn2 = '../data/ABPIC-B_noramp/icdg08r2q_noramp.fits'
    image1 = fits.getdata(fn1, 1)
    image2 = fits.getdata(fn2, 1)
    center1 = [139.3, 222.1]
    #center2 = [129.1, 233.4]
    center2 = center1
    compare_PSF(image1, image2, center1, center2)