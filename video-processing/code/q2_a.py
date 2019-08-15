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

for file in sorted(list_dir):
    filename = os.fsdecode(file)
    if filename.endswith(".png"):
        # open file
        img_YCbCr = Image.open(os.path.join(directory, filename)).convert("YCbCr")

        # set the image as numpy array and extract only Y component
        img_Y = np.array(img_YCbCr)[:, :, Y]

        # calculate entropy and add it to the list
        name = os.path.splitext(filename)[0]
        entropies[0].append(get_entropy(img_Y))
        entropies[1].append(name[-2:])
        # entropies.append((get_entropy(img_Y), name[-2:]))

ind = np.arange(len(entropies[1]))
plt.bar(ind, entropies[0])
plt.xticks(ind, entropies[1])
plt.ylabel("Entropy in bits")
plt.xlabel("Image number")
# plt.plot(entropies)
plt.show()

for pair in list(zip(entropies[1], entropies[0])):
        print(pair)