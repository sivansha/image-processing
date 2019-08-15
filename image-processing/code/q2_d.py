import cv2
import numpy as np

# image loaded
bgr_img1 = cv2.imread('../lena.png')
bgr_img2 = cv2.imread('../northcap.png')

# switch bgr --> grb
rgb_img1 = cv2.cvtColor(bgr_img1, cv2.COLOR_BGR2RGB)
rgb_img2 = cv2.cvtColor(bgr_img2, cv2.COLOR_BGR2RGB)

# calculate number of pixels
pixels_img1 = rgb_img1.shape[0]*rgb_img1.shape[1]
pixels_img2 = rgb_img2.shape[0]*rgb_img2.shape[1]

# calculate histogram for each color
colors = ('R', 'G', 'B')
# variables for holding the R, G, B entropy values for each image
entropy_img1 = [0, 0, 0]
entropy_img2 = [0, 0, 0]

# for each color
for i, color in enumerate(colors):
    # calculate the histogram for each of the i channels
    hist_img1 = cv2.calcHist([rgb_img1], [i], None, [256], [0, 256])
    hist_img2 = cv2.calcHist([rgb_img2], [i], None, [256], [0, 256])

    # calculate entropy for R
    for value in hist_img1:
        # to avoid undefined log behaviour
        if value != 0:
            added_entropy = (value/pixels_img1) * (np.log2(value/pixels_img1))
            entropy_img1[i] += added_entropy
    entropy_img1[i] *= (-1)

    for value in hist_img2:
        # to avoid undefined log behaviour
        if value != 0:
            added_entropy = (value/pixels_img2) * (np.log2(value/pixels_img2))
            entropy_img2[i] += added_entropy
    entropy_img2[i] *= (-1)

print(entropy_img1)
print(entropy_img2)
