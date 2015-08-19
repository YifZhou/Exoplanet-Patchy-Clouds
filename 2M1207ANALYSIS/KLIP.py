#! /usr/bin/env python
from __future__ import print_function, division
import numpy as np
from scipy.io import readsav  # read IDL save file
import matplotlib.pyplot as plt
from astropy.io import fits
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
    R_eff = np.zeros((nImages, len(effIndex)))
    R = np.zeros((nImages, imageCube[0].size))
    for i in range(nImages):
        R_eff[i, :] = imageCube[i].flatten()[effIndex]
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
    target_eff = targetImage.flatten()[effIndex]
    KLBases_eff = KLBases[0:klip, effIndex]
    # project target image on KL_bases
    coeff = np.dot(KLBases_eff, target_eff)
    image = np.zeros(targetImage.shape)
    for i, c in enumerate(coeff):
        image += KLBases[i, :].reshape(targetImage.shape) * c
    return image


def getEffCoord(imShape, annulusList):
    """return index for search region
    exclude region listed in annulusList
    annulusList is an n*4 array, including n annulli
    each annulli centered at annulusList[i][0], annuluslist[i][1]
    inner radius: annlusList[i][2], out radius: annlusList[i][3]
    """
    xx, yy = np.meshgrid(np.arange(imShape[0]), np.arange(imShape[1]))
    mask = np.ones(imShape)
    for annulus in annulusList:
        dist = np.sqrt((xx - annulus[0])**2 + (yy - annulus[1])**2)
        mask[np.where((dist >= annulus[2]) & (dist <= annulus[3]))] = 0
    return np.where(mask == 1)


if __name__ == '__main__':
    savFile = readsav('F125W_KLIP_PSF_library.sav')
    cube0 = savFile['angle0cube']
    cube1 = savFile['angle1cube']
    # get effective coordinate
    coord_eff = getEffCoord(cube0[0].shape, [[17, 9, 0, 4], [17, 9, 10, 100],
                                             [13, 13, 0, 3]])
    id_eff = coord_eff[0] * cube0[0].shape[1] + coord_eff[1]
    Z = KLtrans(cube0, id_eff)
    residual = np.zeros((cube1.shape[0], cube0.shape[0] - 3))
    maxValue = np.zeros((cube1.shape[0], cube0.shape[0] - 3))
    klipList = range(3, cube0.shape[0])
    for i in range(cube1.shape[0]):
        for j, klip in enumerate(klipList):
            im = KLIP(cube1[i], Z, id_eff, klip)
            resIm = cube1[i] - im
            residual[i, j] = np.sqrt((resIm[coord_eff]**2).sum())
            maxValue[i, j] = resIm[8, 16]
    residual0 = np.mean(residual, axis=0)
    maxValue0 = np.mean(maxValue, axis=0)
    plt.close('all')
    fig = plt.figure()
    ax_res = fig.add_subplot(111)
    ax_max = ax_res.twinx()
    l_res, = ax_res.plot(klipList, residual0, label='residual')
    ax_res.set_xlabel('klip')
    ax_res.set_ylabel('Residual')
    l_max, = ax_max.plot(klipList, maxValue0 / maxValue0.max(),
                         label='max value', color='b')
    ax_max.set_ylabel('Max value')
    ls = [l_res, l_max]
    labels = [l.get_label() for l in ls]
    ax_res.legend(ls, labels)
    plt.show()
    fits.writeto('KLIP_test.fits', resIm, clobber=True)
