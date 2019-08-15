from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import os

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

entropies = [[] for i in range(2)]

# load images
# directory = os.fsencode('../images/q2/sintel')
directory = '../images/q2/sintel'
list_dir = os.listdir(directory)
list_dir = sorted([x for x in list_dir if x.endswith(".png")])

for i in range(1, len(list_dir)):
    # open files
    img_YCbCr_current = Image.open(os.path.join(directory, list_dir[i])).convert("YCbCr")
    img_YCbCr_pervious = Image.open(os.path.join(directory, list_dir[i-1])).convert("YCbCr")

    # set the image as numpy array and extract only Y component
    img_YCbCr_current = np.array(img_YCbCr_current)[:, :, Y].astype(np.int32)
    img_YCbCr_pervious = np.array(img_YCbCr_pervious)[:, :, Y].astype(np.int32)

    img_Y_diff = img_YCbCr_current - img_YCbCr_pervious

    # calculate entropy and add it to the list
    name_current = os.path.splitext(list_dir[i])[0]
    name_previous = os.path.splitext(list_dir[i-1])[0]

    # fill in the array
    entropies[0].append(get_entropy(img_Y_diff))
    entropies[1].append(name_current[-2:] + "-" + name_previous[-2:])
    # entropies.append((get_entropy(img_Y), name[-2:]))

ind = np.arange(len(entropies[1]))
plt.bar(ind, entropies[0])
plt.xticks(ind, entropies[1])
plt.ylabel("Entropy of differential image in bits")
plt.xlabel("Difference for images xx and yy")
# plt.plot(entropies)
plt.show()

for pair in list(zip(entropies[1], entropies[0])):
    print(pair)