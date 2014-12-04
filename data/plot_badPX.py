def badPixelRemove(image, dq):
    """
    remove hot pixel or unstable response
    """
    meanImage = (np.roll(image, 1, axis = 0) + np.roll(image, -1, axis = 0) + np.roll(image, 1, axis = 1) + np.roll(image, -1, axis = 1)) #array that the values are the
    #dqbin = ['{0:016b}'.format(i) for i in dq.flat]
    #isBad = np.array([True if dqstr[-5] == '1' or dqstr[-6] == '1' else False for dqstr in dqbin]).reshape(np.shape(dq))
    image[dq == 40] = meanImage[dq == 40]
    return image

if __name__ == '__main__':
    target = 'ABPIC-B'
    file_info = pd.read_csv('ABPIC-B/flt_file_info.csv')
    images = []
    headers = []
    orbit_list = list(set(file_info['orbit']))
    dither_list =  list(set(file_info['dither']))
    for orbit_i, dither_i in [(orbit, dither) for orbit in orbit_list for dither in dither_list]:
        expo_info = file_info[(file_info['orbit'] == orbit_i) & (file_info['dither'] == dither_i)]
        images[:] = []
        headers[:] = []
        for fn in expo_info['file name']:
            fits_content = fits.open(os.path.join(target, fn))
            #images.append(fits_content['SCI'].data)
            image_i = fits_content['sci'].data
            dq = fits_content['dq'].data
            image_i0 = badPixelRemove(image_i, dq)
            images.append(image_i0)
            header = fits_content['primary'].header
            headers.append(fits_content['sci'].header)
            fits_content.close()