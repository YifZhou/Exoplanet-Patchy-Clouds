import glob
import sys
from os import path
from astropy.io import fits

if __name__ == '__main__':
    target = 'ABPIC-B'
    fileType = 'drz'
    fileDIR = path.join('.', target)
    for fn in glob.glob(path.join(fileDIR, '*{0}.fits'.format(fileType))):
        im = fits.getdata(fn, 'sci')
        print fn, 'size: ',im.shape