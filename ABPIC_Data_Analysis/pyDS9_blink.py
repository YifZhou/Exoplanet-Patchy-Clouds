import ds9
import sys
import os
import astropy.io.fits as fits
# def viewImage(fits_name):
#     """
#     function to open fits file and view then image
#     """
#     d = ds9.ds9()
#     fits_content = fits.open(fits_name)
#     target = fits_content[0].header['targname']
#     if target == 'ABPIC-B':
#         planet_coord = '06:19:12.94 -58:03:20.9' # RA and Dec of the planet in FK5 coordinate, data obtained from simbed, for pan the iamge to centered on the target
#     elif target == '2M1207B':
#         planet_coord = '12:07:33.467 -39:32:54.00'
#     else:
#         print 'target missing'
#         return 1
#     d.set(' '.join(['file', fits_name]))
#     d.set('align yes')
#     d.set('contour clear')
#     d.set('cmap Cool')
#     d.set(' '.join(['pan to', planet_coord, 'wcs fk5']))
#     center = [float(num) for num in d.get('pan image').split()]
#     d.set('scale histequ')
#     d.set('scale mode 99.5')
#     d.set('zoom 4')
#     return center

if __name__ == '__main__':
    d = ds9.ds9()
    d.set('blink no')
    d.set('frame delete all')  # intitialize ds9
    file_dir = '/home/yzhou/Documents/Exoplanet_Patchy_Project/data/ABPIC-B'
   
    target = 'ABPIC-B'
    if target == 'ABPIC-B':
        planet_coord = '06:19:12.94 -58:03:20.9'   # RA and Dec of the planet in FK5 coordinate, data obtained from simbed, for pan the iamge to centered on the target
    elif target == '2M1207B':
        planet_coord = '12:07:33.467 -39:32:54.00'
    else:
        print 'target missing'
        exit(1)
    for fileName in sys.argv[1:]:
        print fileName
        d.set('frame new')
        d.set(' '.join(['file', os.path.join(file_dir, fileName)]))
        d.set('align yes')
        d.set('contour clear')
        d.set('cmap Cool')
        d.set(' '.join(['pan to', planet_coord, 'wcs fk5']))
        center = [float(num) for num in d.get('pan image').split()]
        d.set('scale log 2')
        d.set('scale mode 99.5')
        d.set('scale limits 0 10000')
        d.set('zoom 4')

    d.set('match frame physical')
    d.set('match scale')
    d.set('blink yes')
    d.set('blink interval 1')
