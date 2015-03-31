#! /usr/bin/env python
from __future__ import print_function, division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../python_src')
from linearFit import linearFit
"""
print out the shift speed of each orbit with a linear fit
"""

if __name__ == '__main__':
    orbitList = [10, 11, 12]
    dataFrame = pd.read_csv('2015_Feb_27_myfits_aper=5_result.csv', parse_dates = {'datetime':['OBS_DATE', 'OBS_TIME']}, index_col = 'datetime')
    print('{0:^6} {1:^4} {2:>6}'.format('orbit', 'type', 'v'))
    for orbit in orbitList:
        subDF125 = dataFrame[(dataFrame['ORBIT'] == orbit) & (dataFrame['FILTER'] == 'F125W')]
        subDF160 = dataFrame[(dataFrame['ORBIT'] == orbit) & (dataFrame['FILTER'] == 'F160W')]
        t125 = np.float32(subDF125.index.values - subDF125.index.values[0])/(60*60 * 1.e9)
        t160 = np.float32(subDF160.index.values - subDF160.index.values[0])/(60*60 * 1.e9)
        x0125, Vx125, sigb, sigm, chisqX125 = linearFit(t125, subDF125['XCENTER'].values)
        y0125, Vy125, sigb, sigm, chisqY125 = linearFit(t125, subDF125['YCENTER'].values)
        x0160, Vx160, sigb, sigm, chisqX160 = linearFit(t160, subDF160['XCENTER'].values)
        y0160, Vy160, sigb, sigm, chisqY160 = linearFit(t160, subDF160['YCENTER'].values)
        print('{0:^6d} {1:^4} {2:>.5f}'.format(orbit, 'X', (Vx125 + Vx160)/2))
        print('{0:^6d} {1:^4} {2:>.5f}'.format(orbit, 'Y', (Vy125 + Vy160)/2))
        print('*'*20)
        plt.close('all')
        fig = plt.figure()
        axX = fig.add_subplot(121)
        axY = fig.add_subplot(122, sharey = axX)
        axX.plot(t125, t125*Vx125, label = 'F125, v={0:0.4f}'.format(Vx125), color = 'r')
        axX.plot(t125, subDF125['XCENTER'] - x0125, '.', color = 'r')
        axX.plot(t160, t160*Vx160, label = 'F160, v={0:0.4f}'.format(Vx160), color = 'b')
        axX.plot(t160, subDF160['XCENTER'] - x0160, '.', color = 'b')
        axY.plot(t125, t125*Vy125, label = 'F125, v={0:0.4f}'.format(Vy125), color = 'r')
        axY.plot(t125, subDF125['YCENTER'] - y0125, '.', color = 'r')
        axY.plot(t160, t160*Vy160, label = 'F160, v={0:0.4f}'.format(Vy160), color = 'b')
        axY.plot(t160, subDF160['YCENTER'] - y0160, '.', color = 'b')
        axX.set_title('X')
        axY.set_title('Y')
        for ax in [axX, axY]:
            ax.set_xlabel('time (h)')
            ax.set_ylabel('shfit (pixel)')
            ax.legend()
        fig.tight_layout()
        fig.savefig('shift_speed_orbit_{0}.pdf'.format(orbit))
        