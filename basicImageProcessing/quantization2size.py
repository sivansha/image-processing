import cv2
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np

def quantize(img, step):
    if step != 0:
        # take every entry in matrix and perform a whole number division on every element by the number of steps
        # multiply again to receive the floor value for each entry 
        return (img // step) * step
    else:
        return img

def get_entropy(img):
    # calculate number of pixels
    pixels = img.shape[0]*img.shape[1]

    # get histogramm
    edges, hist = np.unique(img.flatten(), return_counts=True)

    # Y entropy
    entropy = 0

    # calculate entropy
    for c in hist:
        entropy += (c/pixels) * (np.log2(c/pixels))
    entropy *= (-1)

    return entropy
##############################################################################

Y, Cb, Cr = 0, 1, 2

# load image
img_YCbCr = Image.open("./lena.png").convert("YCbCr")

# set the images as numpy array
img_asArray = np.array(img_YCbCr)

# get only Y component
img_Y = img_asArray[:, :, Y]

# different quantization steps, 0 means perform no quantization at all
quantization_steps = [0, 2, 5, 10, 20, 50]
# counter for quantization step
k = 0

# plot 6 images as 2 rows, each 3 columns
fig, axes = plt.subplots(2, 3)

# visual improvement
plt.subplots_adjust(hspace = 0.31)

# iterate over all axes, in .flatten (1d array) manner
for i, ax in enumerate(axes.flat):
    # perform quantization on Y component
    result = quantize(img_Y, quantization_steps[k])

    # count overall amount of pixels
    pixels = result.shape[0]*result.shape[1]

    # plot image with matplotlib
    ax.imshow(result, cmap='gray')

    # calculate entropy
    e = get_entropy(result)

    # set labels on plot
    ax.text(-10, -10, "Quantization step = {0}".format(quantization_steps[k]))
    ax.set_xlabel("Entropy = {0:.4f}\nEstimated filesize = {1:.4f} KB".format(e, (e*pixels)/(8*1024)))

    # iterate over quantization steps
    k += 1

plt.show()


