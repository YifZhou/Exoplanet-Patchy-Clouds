import ds9
import sys
import os

if __name__ == '__main__':
    fileName = sys.argv[1]
    d = ds9.ds9()
    d.set('file {0}'.format(os.path.join(os.getcwd(), fileName)))
    d.set('scale limits 0.95 1.05')
    d.set('pan to 500 600 physical')
    d.set('zoom 4')
    x = [473.78, 483.88, 473.78, 483.88, 508.18, 518.32, 508.18, 518.32]
    y = [587.07, 587.07, 598.30, 598.30, 601.11, 601.11, 612.50, 612.50]
    for xi, yi in zip(x, y):
        print "regions command '{{image; circle {0} {1} 5}}'".format(xi-5, yi-5)
        d.set('regions', 'image; circle({0}, {1}, 5)'.format(xi-5, yi-5))
    