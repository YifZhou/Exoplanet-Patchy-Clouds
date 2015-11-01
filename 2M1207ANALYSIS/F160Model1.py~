from pymc import Uniform, deterministic, Normal
import numpy as np

t160, F160B = np.loadtxt('F160_data.dat', usecols=(0, 2), unpack=True)
sigma160 = 0.0112


amplitude = Uniform('amplitude', lower=0, upper=0.05)
period = Uniform('period', lower=2, upper=40, doc='period of sinusoid')
phase = Uniform('phase', lower=0, upper=2 * np.pi)


@deterministic(plot=False)
def count(Amp=amplitude, T=period, Phase=phase):
    return Amp * np.sin((2 * np.pi / T) * t160 + Phase) + 1

lcModel = Normal('light curve', mu=count, tau=1. / sigma160**2, value=F160B,
                 observed=True)
