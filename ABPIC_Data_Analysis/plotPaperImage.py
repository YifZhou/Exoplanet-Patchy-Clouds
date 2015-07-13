import matplotlib.pyplot as plt
import aplpy
import numpy as np


plt.close('all')
# fig = plt.figure()
# gc = aplpy.FITSFigure('original.fits', hdu = 1, figure = fig)

# gc.show_colorscale(cmap = 'hot',
# interpolation = 'bicubic',vmin=-50, vmax = 2000, stretch = 'arcsinh')
# ax = plt.gca()
# ax.set_xlim([44, 184])
# ax.set_ylim([98, 238])
# plt.savefig('original.pdf')
fig1 = plt.figure()
gc = aplpy.FITSFigure('subtracted.fits', hdu=1, figure=fig1)

gc.show_colorscale(
    cmap='hot', interpolation='bicubic',
    vmin=-50, vmax=2000, stretch='arcsinh')
ax = plt.gca()

cen = [114.212, 169.284]
seccen1 = [94.78, 208.07]
seccen2 = [114.28, 213.83]

xx, yy = np.meshgrid(range(256), range(256))
dist = np.sqrt((xx - cen[0])**2 + (yy - cen[1])**2)
dist1 = np.sqrt((xx - seccen1[0])**2 + (yy - seccen1[1])**2)
dist2 = np.sqrt((xx - seccen2[0])**2 + (yy - seccen2[1])**2)

mask = np.ones((256, 256))
mask[(dist >= 30) & (dist <= 60)] = 0
mask[dist1 <= 10] = 1
mask[dist2 <= 10] = 1

# ax.contourf(xx, yy, mask, 3,
# colors = [(0,0,0,0), '0.2', '0.3'], hatches = ['o', None, None],
# alpha = 0.5, antialiased = True)
ax.contour(mask, levels=[-0.1, 0.9], antialiased=True, lw=0.8, colors='white')
ax.set_xlim([44, 184])
ax.set_ylim([99, 239])
plt.savefig('subtracted.pdf')
