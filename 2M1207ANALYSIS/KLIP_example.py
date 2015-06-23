#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
"""example script written by Neil Zimmerman
"""


def get_klip_basis(R, cutoff):
    w, V = np.linalg.eig(np.dot(R, np.transpose(R)))
    # indices of eigenvals sorted in descending order
    sort_ind = np.argsort(w)[::-1]
    # column of ranked singular values
    sv = np.sqrt(w[sort_ind]).reshape(-1, 1)
    Z = np.dot(1. / sv * np.transpose(V[:, sort_ind]), R)
    return Z[0:cutoff, :], sv
