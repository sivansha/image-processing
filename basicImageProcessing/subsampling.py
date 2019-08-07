import numpy as np
from PIL import Image

Y, Cb, Cr = 0, 1, 2

# load image and convert to YCbCr
img = Image.open('./lena.png')
img_ycbcr = img.convert('YCbCr')

# calculate number of pixels
pixels = img_ycbcr.size[0] * img_ycbcr.size[1]

# read image to array
img_asArray = np.array(img_ycbcr)

# 444 - no subsampling
img_ycbcr_444 = img_asArray.copy()

#422
img_ycbcr_422 = img_asArray.copy()
# subsample to 422
for c in img_ycbcr_422[:, :, 1:3]:
    i = 0
    for p in c:
        if i%2 == 0:
            temp = p
        else:
            p[0] = temp[0]
            p[1] = temp[1]
        i += 1
#420
img_ycbcr_420 = img_asArray.copy()
# subsample to 420
i = 0
temp = list()
for c in img_ycbcr_420[:, :, 1:3]:
    if i%2 != 0:
        temp = c[0]
        for p in c:
            p[0] = temp[0]
            p[1] = temp[1]
    else:
        j = 0
        for p in c:
            if j%2 == 0:
                temp = p
            else:
                p[0] = temp[0]
                p[1] = temp[1]
            j += 1
    i += 1

# re-create the images from array
images = [Image.fromarray(img_ycbcr_444[:, :, :], "YCbCr"), Image.fromarray(img_ycbcr_422[:, :, :], "YCbCr"), Image.fromarray(img_ycbcr_420[:, :, :], "YCbCr")]
# array for the histograms
histograms = list()
# prints each of the sub-sampled images
for img in images:
    img.show()
    histograms.append(img.histogram())


# variables for holding the Y, Cr, Cb entropy values for each image
entropies = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

# calculate histograms
for i, hist in enumerate(histograms):
    # calculate hist Y
    histY = hist[0:256]
    for value in histY:
        # to avoid undefined log behaviour
        if value != 0:
            added_entropy = (value/pixels) * (np.log2(value/pixels))
            entropies[i][Y] += added_entropy
    entropies[i][Y] *= (-1)

    # calculate hist Cb
    histCb = hist[256:512]
    for value in histCb:
        # to avoid undefined log behaviour
        if value != 0:
            added_entropy = (value/pixels) * (np.log2(value/pixels))
            entropies[i][Cb] += added_entropy
    entropies[i][Cb] *= (-1)

    # calculate hist Cr
    histCr = hist[512:768]
    for value in histCr:
        # to avoid undefined log behaviour
        if value != 0:
            added_entropy = (value/pixels) * (np.log2(value/pixels))
            entropies[i][Cr] += added_entropy
    entropies[i][Cr] *= (-1)

for ent in entropies:
    print(ent)
