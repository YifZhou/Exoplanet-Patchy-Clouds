#! /usr/bin/env python
"""
classify the fits file
based on source name
"""

import glob
import sys
import os
from astropy.io import fits

def classify(source_name):
    """
    classify fits file based on input
    para: source_name
    """
    maindir = os.path.dirname(__file__)
    subdir = os.path.join(maindir, source_name)
    if not os.path.exists(subdir):
        os.makedirs(subdir)
    #for fits_file in glob.glob('*.fits')
    for fits_file in glob.glob('*.fits'):
        fits_content = fits.open(fits_file)
        try:
            if fits_content[0].header['targname'] == source_name:
                fits_content.close()
                new_name = os.path.join(subdir, fits_file)
                os.rename(fits_file, new_name)
                print 'moved file {0}'.format(fits_file)
        except KeyError:
            pass
        finally:
            fits_content.close()
            
                               

if __name__ == '__main__':
    classify(sys.argv[1])




