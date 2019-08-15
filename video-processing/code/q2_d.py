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

def CF1(diff):
    return np.mean(diff)

def CF2(diff):
    return np.mean(np.abs(diff))
    
def EstMotion(next, current, cost_func, step = 16, p = 7):
    # step = 16
    iLen, jLen = next.shape
    prediction = np.zeros(next.shape, dtype = np.int32)
    locations = []
    distances = []


    for i in range(0, iLen, step):
        for j in range(0, jLen, step):
            # best_hit, (posX, posY) = find_best_hit(\
            # next[i:i+step, j:j+step], \
            # current[i-p:i+step+p, j-p:j+step+p], \
            # step, \
            # cost_func, \
            # p)

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
                        # d = [k-i, m-j]
                        
            
            
            # (x, y) = i - posX, j - posY

            locations.append(l)
            distances.append(d)
            prediction[i:i+step, j:j+step] = best_hit


    
    return distances, locations, prediction

##############################################################################

Y, Cb, Cr = 0, 1, 2

entropies = [[] for i in range(2)]

# load images
# directory = os.fsencode('../images/q2/sintel')
directory = '../images/q2/sintel'
list_dir = os.listdir(directory)
list_dir = sorted([x for x in list_dir if x.endswith(".png")])

prev = None

for i in range(len(list_dir) - 1):
    # open files
    img_YCbCr_current = Image.open(os.path.join(directory, list_dir[i])).convert("YCbCr")
    img_YCbCr_next = Image.open(os.path.join(directory, list_dir[i + 1])).convert("YCbCr")

    # set the image as numpy array and extract only Y component
    img_YCbCr_current = np.array(img_YCbCr_current)[:, :, Y].astype(np.int32)
    img_YCbCr_next = np.array(img_YCbCr_next)[:, :, Y].astype(np.int32)

    if prev is not None:
        img_YCbCr_current = prev

    ds, ls, img_YCbCr_prediction = EstMotion(img_YCbCr_next, img_YCbCr_current, CF2, p=7, step=16)

    # img_YCbCr_diff = img_YCbCr_next - img_YCbCr_prediction ???

    # plot 3 images as 3 rows, each 1 column
    fig, axes = plt.subplots(1, 1)

    axes.set_xlabel("Entropy = {0:.4f}".format(get_entropy(img_YCbCr_prediction)))
    x,y,dx,dy = [x[0] for x in ls], [x[1] for x in ls], [x[0] for x in ds], [x[1] for x in ds]
    axes.quiver(y, x, dy, dx)
    # axes.quiver(y, x, dy, dx, angles='xy', scale_units='xy', scale=1) # precise pixel to pixel movement
    axes.imshow(img_YCbCr_prediction, cmap = 'gray')

    plt.show()

    prev = img_YCbCr_prediction

    # calculate entropy and add it to the list
    name_current = os.path.splitext(list_dir[i])[0]
    name_next = os.path.splitext(list_dir[i])[0]


# ind = np.arange(len(entropies[1]))
# plt.bar(ind, entropies[0])
# plt.xticks(ind, entropies[1])
# plt.plot(entropies)
# plt.show()

# for pair in list(zip(entropies[1], entropies[0])):
#     print(pair)