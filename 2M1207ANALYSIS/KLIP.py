#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
from scipy.io import readsav  # read IDL save file

"""KLIP pipe line
   reference:  Sourmer 2012
"""


def KLtrans(targetImage, imageCube):
    """
    Keyword Arguments:
    imageCube -- PSF library, i*j*n, i and j are dimensions of the image,
                 n is the number of images.
    targetImage -- the targetImage to be transformed
    """
    nImages = imageCube.shape[-1]  # number of images saved in the imageCube
    E = np.zeros((nImages, nImages))
