#!/usr/bin/env python3
# -*- coding: utf-8 -*

import cv2
import numpy as np
from matplotlib import pyplot as plt

# load image
bgr_img1 = cv2.imread('../lena.png')
# convert images to yuv format
yuv_img1=cv2.cvtColor(bgr_img1, cv2.COLOR_BGR2YUV)

# extract y chanel
yuv_img1_asArray = np.array(yuv_img1)
y_img_as_array = yuv_img1_asArray[:, :, 0]

# compute discrete Fourier Transform:
fft2_img1 = np.fft.fft2(y_img_as_array)
# convert to abs values:
abs_fft = np.log(np.abs(fft2_img1))

# perform shift on th discrete Fourier Transform:
fft2_fftshift_img1 = np.fft.fftshift(fft2_img1)
# convert to abs values:
abs_fft_fftshift = np.log(np.abs(fft2_fftshift_img1))

# plotting the hist and pictures
fig, ax = plt.subplots(nrows=1, ncols=2)
ax[0].imshow(abs_fft, cmap = 'gray')
ax[0].set_title('dft')
ax[1].imshow(abs_fft_fftshift, cmap = 'gray')
ax[1].set_title('dft shifted')
plt.show()
