#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
"""sqaure Mean
"""


def squareMean(a):
    return np.sqrt((np.array(a)**2).mean())
