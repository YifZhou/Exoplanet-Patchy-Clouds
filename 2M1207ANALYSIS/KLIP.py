#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
from scipy.io import readsav  # read IDL save file
import matplotlib.pyplot as plt
"""KLIP pipe line
   reference:  Sourmer 2012
adapted from Neil Zimmerman's code
"""


def KLtrans(imageCube, effIndex):
    """
    Keyword Arguments:
    imageCube -- PSF library, i*j*n, i and j are dimensions of the image,
                 n is the number of images.
    effIndex -- the index to define the search Area
    """
    nImages = imageCube.shape[0]  # number of images saved in the imageCube
    # establish R array
    # for _eff, only non-masked value counts
    # on the other hand, for R, every value conts
    R_eff = np.zeros((nImages, len(effIndex[0])))
    R = np.zeros((nImages, imageCube[0].size))
    for i in range(nImages):
        R_eff[i, :] = imageCube[i][effIndex].flatten()
        R[i, :] = imageCube[i].flatten()
    eigens, vectors = np.linalg.eig(np.dot(R_eff, R_eff.T))
    # sort by eigen values, get the index from large to small
    sort_ind = np.argsort(eigens)[::-1]
    sv = np.sqrt(eigens[sort_ind]).reshape(-1, 1)
    Z = np.dot(1 / sv * np.transpose(vectors[:, sort_ind]), R)
    # sv = np.sqrt(w[sort_ind]).reshape(-1, 1)
    # Z = np.dot(1. / sv * np.transpose(V[:, sort_ind]), R)
    return Z


def KLIP(targetImage, KLBases, effIndex, klip):
    """main function to carry out KLIP algorithm
    targetImage -- the image needs primary subtraction
    KLBases -- KL base matrix calculated by KLtrans
    effIndex -- effective index to discrbie the search area
    klip -- number of principle component to use
    """
    target_eff = targetImage[effIndex].flatten()
    KLBases_eff = KLBases[0:klip, effIndex]
    # project target image on KL_bases
    coeff = np.dot(KLBases_eff, target_eff)
    image = np.zeros(targetImage.shape)
    for i, c in enumerate(coeff):
        image += KLBases[i, :].reshape(targetImage.shape)
    return image


def getEffIndex(imShape, center, radiusList):
    """calculate search region Index
    """
    xx, yy = np.meshgrid(np.arange(imShape[0]), np.arange(imShape[1]))
    dist = np.sqrt((xx - center[0])**2 + (yy - center[1])**2)
    dim1_eff = []
    dim2_eff = []  # use dimension 1 and 2 instead of x and y
    for rPair in radiusList:
        xi, yi = np.where((dist > rPair[0]) & (dist < rPair[1]))
        dim1_eff.append(xi)
        dim2_eff.append(yi)
    return np.concatenate(dim1_eff), np.concatenate(dim2_eff)


if __name__ == '__main__':
    savFile = readsav('F125W_KLIP_PSF_library.sav')
    cube0 = savFile['angle0cube']
    cube1 = savFile['angle1cube']
    id_eff = getEffIndex(cube0[0].shape, [17, 9], [[6.5, 10]])
    Z = KLtrans(cube0, id_eff)
    im = KLIP(cube1[0], Z, id_eff, 20)
