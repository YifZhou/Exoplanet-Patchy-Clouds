import F125Model
from pymc import MCMC
import visualMCMC
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

plt.style.use('paper')


def gauss(x, a, x0, sigma):
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2))

M = MCMC(F125Model)
M.sample(iter=1000000, burn=1000, thin=10)

title = 'F125W: include Orbit 1'
plt.close('all')
p = visualMCMC.visualMCMC(M.trace('period')[:],
                          M.trace('amplitude')[:] * 100,
                          xlim=[5, 25], ylim=[0, 2.5], color='b')
p.set_axis_labels('Period [h]', 'Amplitude [%]')

# calculate the 1 sigma error for period and amplitude
pBins = np.linspace(6, 40, 171)
midBins = (pBins[:-1] + pBins[1:]) / 2
dBin = pBins[1] - pBins[0]
pcount, pBin = np.histogram(M.trace('period')[:], bins=pBins, normed=1)
p0 = midBins[pcount == pcount.max()][0]


p_floor = midBins[(pcount <= 0.60 * pcount[midBins == p0]) &
                  (midBins < p0)][-1]
p_ceil = midBins[(pcount <= 0.60 * pcount[midBins == p0]) & (midBins > p0)][0]

aBins = np.linspace(0.00, 0.025, 51) * 100
midBins = (aBins[:-1] + aBins[1:]) / 2
aCount, aBin = np.histogram(
    M.trace('amplitude')[:] * 100, bins=aBins, normed=1)
gpAmp, cov = curve_fit(gauss, midBins,
                       aCount, p0=[aCount.max(), 1, 0.5])


fig = plt.gcf()
fig.axes[0].text(0.02, 0.05, title, transform=fig.axes[0].transAxes)
p_low = '{0:.2f}'.format(p0 - p_floor)
p_high = '{0:.2f}'.format(p_ceil - p0)
fig.axes[0].text(0.02, 0.85, r'$p = {0:.2f}^{{+{1:.2f}}}_{{-{2:.2f}}}$'
                 .format(p0, p_ceil - p0, p0 - p_floor) + '\n' +
                 r'$A = ({0:.2f} \pm {1:.2f})\%$'.format(gpAmp[1], gpAmp[2]),
                 transform=fig.axes[0].transAxes)
plt.tight_layout()
plt.show()
plt.savefig(title.replace(" ", "") + '.pdf')
