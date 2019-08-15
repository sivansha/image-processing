#!/usr/bin/env python3
# -*- coding: utf-8 -*

import cv2
import numpy as np
from matplotlib import pyplot as plt

# load image and convert it to YUV:
bgr_img1 = cv2.imread('../lena.png')
yuv_img1 = cv2.cvtColor(bgr_img1, cv2.COLOR_BGR2YUV)
# extract the Y channel:
yuv_img1_asArray = np.array(yuv_img1)
y_img_as_array = yuv_img1_asArray[:, :, 0]

# Adding Gaussian noise: µ = 0; σ = 10
img_gaussian_noise1 = y_img_as_array + np.random.normal(0, 10, y_img_as_array.shape)
# transform the image to the frequency domain (dft):
fft2_img_gaussian_noise1 = np.fft.fft2(img_gaussian_noise1)
fft2_img_gaussian_noise1 = np.log(np.abs(fft2_img_gaussian_noise1))

# Adding Gaussian noise: µ = 0; σ = 50
img_gaussian_noise2 = y_img_as_array + np.random.normal(0, 50, y_img_as_array.shape)
# transform the image to the frequency domain (dft):
fft2_img_gaussian_noise2 = np.fft.fft2(img_gaussian_noise2)
fft2_img_gaussian_noise2 = np.log(np.abs(fft2_img_gaussian_noise2))


# plotting the hist and pictures
fig, ax = plt.subplots(nrows=2, ncols=2)
ax[0, 0].imshow(img_gaussian_noise1, cmap = 'gray')
ax[0, 0].set_title('gaussian noise, sigma=10')
ax[1, 0].imshow(fft2_img_gaussian_noise1, cmap = 'gray')
ax[1, 0].set_title('dft, sigma=10')
ax[0, 1].imshow(img_gaussian_noise2, cmap = 'gray')
ax[0, 1].set_title('gaussian noise, sigma=50')
ax[1, 1].imshow(fft2_img_gaussian_noise2, cmap = 'gray')
ax[1, 1].set_title('dft, sigma=50')

plt.show()
