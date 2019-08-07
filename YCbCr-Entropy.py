from PIL import Image
import numpy as np

Y, Cb, Cr = 0, 1, 2

# load images and converts them to YCbCr
img1 = Image.open("./lena.png").convert("YCbCr")
img2 = Image.open("./northcap.png").convert("YCbCr")

# calculate number of pixels
pixels = [img1.size[0]*img1.size[1], img2.size[0]*img2.size[1]]

# calculate histogram for each image
histograms = [img1.histogram(), img2.histogram()]

# variables for holding the Y, Cr, Cb entropy values for each image
entropies = [[0, 0, 0], [0, 0, 0]]

# calculate histograms
for i, hist in enumerate(histograms):
    # calculate hist Y
    histY = hist[0:256]
    for value in histY:
        # to avoid undefined log behaviour
        if value != 0:
            added_entropy = (value/pixels[i]) * (np.log2(value/pixels[i]))
            entropies[i][Y] += added_entropy
    entropies[i][Y] *= (-1)

    # calculate hist Cb
    histCb = hist[256:512]
    for value in histCb:
        # to avoid undefined log behaviour
        if value != 0:
            added_entropy = (value/pixels[i]) * (np.log2(value/pixels[i]))
            entropies[i][Cb] += added_entropy
    entropies[i][Cb] *= (-1)

    # calculate hist Cr
    histCr = hist[512:768]
    for value in histCr:
        # to avoid undefined log behaviour
        if value != 0:
            added_entropy = (value/pixels[i]) * (np.log2(value/pixels[i]))
            entropies[i][Cr] += added_entropy
    entropies[i][Cr] *= (-1)

print(entropies[0])
print(entropies[1])
