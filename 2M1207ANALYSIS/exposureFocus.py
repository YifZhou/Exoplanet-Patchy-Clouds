#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline as splineFunc
import pickle

"""using WFC3 focus data to calculate the focus for tinytim modeling
"""
def exposureFocus(MJD0):
    """
    the spline function is saved in a pickle file
    """
    focus0 = -0.24
    MJD, focus = np.loadtxt('focus.dat', usecols = (0, 5), unpack = True)
    spline = splineFunc(MJD, focus)
    #spline = pickle.load(open('focus_splineFunc.pkl', 'rb'))
    #pickle.dump(spline, open('focus_splineFunc.pkl', 'wb'))
    import matplotlib.pyplot as plt
    newMJD = np.linspace(min(MJD), max(MJD), 100*len(MJD))
    newFocus = spline(newMJD)
    plt.plot(MJD, focus, '+')
    plt.plot(newMJD, newFocus)
    plt.show()
    return focus0 + spline(MJD0)
    
if __name__ == '__main__':
    print(exposureFocus(5.658166402457E+04))