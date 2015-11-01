#! /usr/bin/env python
from __future__ import print_function, division
import seaborn as sns

"""visualize the MCMC result
"""

sns.set(style="white", color_codes=False)


def visualMCMC(data1, data2, xlim=None, ylim=None, color='b'):
    dist2d = sns.jointplot(data1, data2, xlim=xlim, ylim=ylim,
                           stat_func=None, kind='hex', color=color,
                           marginal_kws=dict(bins=40),
                           joint_kws=dict(bins=40))

    return dist2d
