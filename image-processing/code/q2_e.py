from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

Y, Cb, Cr = 0, 1, 2

# load images and converts them to YCbCr
img1_YCbCr = Image.open("../lena.png").convert("YCbCr")
img2_YCbCr = Image.open("../northcap.png").convert("YCbCr")

# TASK A: show the Y, Cb, Cr components
# set the images as numpy array
img1_asArray = np.array(img1_YCbCr)
img2_asArray = np.array(img2_YCbCr)

# display each of the 3 channels
Image.fromarray(img1_asArray[:, :, Y], "L").show()
Image.fromarray(img1_asArray[:, :, Cb], "L").show()
Image.fromarray(img1_asArray[:, :, Cr], "L").show()
Image.fromarray(img2_asArray[:, :, Y], "L").show()
Image.fromarray(img2_asArray[:, :, Cb], "L").show()
Image.fromarray(img2_asArray[:, :, Cr], "L").show()

# TASK B: show the Y, Cb, Cr distribution
# calculate histogram
hist1 = img1_YCbCr.histogram()
hist2 = img2_YCbCr.histogram()

histograms = list()
histograms.append(hist1)
histograms.append(hist2)

# plot Y, Cb, and Cr distribution
for hist in histograms:
    plt.plot(hist[0:256],   color='K', label="Y value")
    plt.plot(hist[256:512], color='B', label="Cb value")
    plt.plot(hist[512:768],   color='R', label="Cr value")
    plt.legend(loc='upper left')
    plt.title('distributions of YCbCr component’s intensities')
    plt.ylabel('Pixels')
    plt.xlabel('Y, Cb, Cr values')
    plt.show()
