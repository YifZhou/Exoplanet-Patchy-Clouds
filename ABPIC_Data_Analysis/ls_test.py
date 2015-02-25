import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

A = 2.
w = 2.5
T = 2*np.pi/w
phi = 0.5 * np.pi
nin = 1000
nout = 100000
frac_points = 0.9
r = np.random.rand(nin)
x = np.linspace(0.01, 10*np.pi, nin)
x = x[r >= frac_points]
normval = x.shape[0] # For normalization of the periodogram

y = A * np.sin(w*x+phi)
f = np.linspace(0.01, 10, nout)

pgram = signal.lombscargle(x, y, f)
plt.subplot(2, 1, 1)

plt.plot(x%T, y, 'b+')
plt.subplot(2, 1, 2)

plt.plot(f, np.sqrt(4*(pgram/normval)))

plt.show()