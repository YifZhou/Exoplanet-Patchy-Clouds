#! /usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    fn = 'cubic3_shiftchange.dat'
    fn1 = 'fshift_shiftchange.dat'
    stepLength, abs_change, flux_change = np.loadtxt(fn, unpack = True, comments = ';')
    stepLength, abs_change1, flux_change1 = np.loadtxt(fn1, unpack = True)
    fig, axes = plt.subplots(figsize = (8, 4), ncols = 2)
    axes[0].plot(stepLength, abs_change, label = 'cubic3')
    axes[0].plot(stepLength, abs_change1, label = 'fshift')
    axes[0].set_title('RMS change')
    axes[1].plot(stepLength, flux_change, label = 'cubic3')
    axes[1].plot(stepLength, flux_change1, label = 'fshift')
    axes[1].set_title('Flux change')
    for ax in axes:
        ax.legend(loc = 'best')
        ax.set_xlabel('Shift length (pixels)')
        ax.set_ylabel('value change per pixel')

    fig.tight_layout()
    plt.savefig('test_shift.pdf')
    plt.close(fig)
    