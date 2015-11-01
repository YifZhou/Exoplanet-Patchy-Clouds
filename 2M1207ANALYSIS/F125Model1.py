from pymc import Uniform, deterministic, Normal, MCMC
import numpy as np

t125, F125B = np.loadtxt('F125_data1.dat', usecols=(0, 2), unpack=True)
sigma125 = 0.0134


amplitude = Uniform('amplitude', lower=0, upper=0.05)
period = Uniform('period', lower=2, upper=40, doc='period of sinusoid')
phase = Uniform('phase', lower=0, upper=2 * np.pi)


@deterministic(plot=False)
def count(Amp=amplitude, T=period, Phase=phase):
    return Amp * np.sin((2 * np.pi / T) * t125 + Phase) + 1

lcModel = Normal('light curve', mu=count, tau=1. / sigma125**2, value=F125B,
                 observed=True)
