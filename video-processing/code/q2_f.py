from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import os

def get_entropy(img):
    # calculate number of pixels
    pixels = img.size

    # get histogramm
    edges, hist = np.unique(img.flatten(), return_counts=True)

    # Y entropy
    entropy = 0

    # calculate entropy
    for c in hist:
        entropy += (c/pixels) * (np.log2(c/pixels))
    entropy *= (-1)

    return entropy

def get_entropy_vector(img):
    # calculate number of pixels
    pixels = len(img)

    # get histogramm
    edges, hist = np.unique(img, return_counts=True, axis=0)

    # Y entropy
    entropy = 0

    # calculate entropy
    for c in hist:
        entropy += (c/pixels) * (np.log2(c/pixels))
    entropy *= (-1)

    return entropy

def CF1(current):
    return np.mean(current)

def CF2(current):
    return np.mean(np.abs(current))
    
def EstMotion(next, current, cost_func, step = 16, p = 7):
    # step = 16
    iLen, jLen = next.shape
    prediction = np.zeros(next.shape, dtype = np.int32)
    locations = []
    distances = []


    for i in range(0, iLen, step):
        for j in range(0, jLen, step):
            next_block = next[i:i+step, j:j+step]
            # search area
            sa = (i-p,i+p), (j-p,j+p) 
            min_cost = np.inf
            best_hit = None
            l = [i,j]
            d = [0,0]

            for k in range(sa[0][0], sa[0][1]):
                for m in range(sa[1][0], sa[1][1]):
                    search_block = current[k:k+step, m:m+step]

                    if search_block is None or search_block.shape != next_block.shape:
                        continue
                    diff = next_block - search_block
                    t = cost_func(diff)
                    if t < min_cost:
                        min_cost = t
                        best_hit = search_block
                        d = [k-i, j-m]

            locations.append(l)
            distances.append(d)
            prediction[i:i+step, j:j+step] = best_hit


    
    return distances, locations, prediction

##############################################################################

Y, Cb, Cr = 0, 1, 2

entropies = [[] for i in range(2)]

bs = [4, 8, 12, 16, 24, 32]

# load images
directory = '../images/q2/sintel'
list_dir = os.listdir(directory)
list_dir = sorted([x for x in list_dir if x.endswith(".png")])

# CF2

i = 0

for block_size in bs:
    img_YCbCr_current = Image.open(os.path.join(directory, list_dir[i])).convert("YCbCr")
    img_YCbCr_next = Image.open(os.path.join(directory, list_dir[i + 1])).convert("YCbCr")

    # set the image as numpy array and extract only Y component
    img_YCbCr_current = np.array(img_YCbCr_current)[:, :, Y].astype(np.int32)
    img_YCbCr_next = np.array(img_YCbCr_next)[:, :, Y].astype(np.int32)

    ds, ls, img_YCbCr_prediction = EstMotion(img_YCbCr_next, img_YCbCr_current, CF2, p=5, step=block_size)

    img_YCbCr_diff = img_YCbCr_next - img_YCbCr_prediction

    print("Block size: {0}".format(block_size))
    print("Prediction error CF2: {0}".format(get_entropy(img_YCbCr_diff)))
    print("Data units to be transmitted: {0}\n".format(get_entropy_vector(ds) * len(ds)))

