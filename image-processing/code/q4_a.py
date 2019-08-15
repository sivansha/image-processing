import cv2
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np

Y, Cb, Cr = 0, 1, 2

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
    
#########################

# load image
img_YCbCr = Image.open("../lena.png").convert("YCbCr")

# set the images as numpy array
img_asArray = np.array(img_YCbCr)

# get only Y component
img_Y = img_asArray[:, :, Y]

# calculate entropy of the image
e = get_entropy(img_Y)

# calculate total amount of pixels
pixels = img_Y.shape[0] * img_Y.shape[1]

# print	
plt.imshow(img_Y, cmap='gray')
plt.title("Entropy = {0}".format(e))
plt.suptitle("Estimated filesize = {0} KB".format((e*pixels)/(8*1024)))
plt.show()

