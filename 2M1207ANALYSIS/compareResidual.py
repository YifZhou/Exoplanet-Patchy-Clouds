from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
def readPSF(fn):
    im = fits.getdata(fn, 0)
    psf = fits.getdata(fn, 1)
    return im - psf

fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

fn = ['icdg01zdq', 'icdg01zeq', 'icdg01zfq', 'icdg01znq']
axes = [ax1, ax2, ax3, ax4]
for i in range(4):
    psf = np.arcsinh(readPSF('./fitsResult/' + fn[i] +'.fits'))
    axes[i].imshow(psf)

plt.show()

