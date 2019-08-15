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

# returns different T matrix depending on block size
def get_T(block_size):
    T = None
    if block_size == "1x2" or block_size == "2x2":
        T = np.array([[1, 1], [1, -1]], dtype = np.float64)
        T *= (1.0/np.sqrt(2))
    elif block_size == "4x4":
        T = np.array([\
        [1, 1, 1, 1], \
        [1, 1, -1, -1], \
        [np.sqrt(2), -np.sqrt(2), 0, 0], \
        [0, 0, np.sqrt(2), -np.sqrt(2)]], \
        dtype = np.float64)
        T *= 1.0/2.0
    elif block_size == "8x8":
        T = np.array([\
        [1, 1, 1, 1, 1, 1, 1, 1], \
        [1, 1, 1, 1, -1, -1, -1, -1], \
        [np.sqrt(2), np.sqrt(2), -np.sqrt(2), -np.sqrt(2), 0, 0, 0, 0], \
        [0, 0, 0, 0, np.sqrt(2), np.sqrt(2), -np.sqrt(2), -np.sqrt(2)], \
        [2, -2, 0, 0, 0, 0, 0, 0], \
        [0, 0, 2, -2, 0, 0, 0, 0], \
        [0, 0, 0, 0, 2, -2, 0, 0], \
        [0, 0, 0, 0, 0, 0, 2, -2] \
        ], dtype = np.float64)
        T *= 1.0/np.sqrt(8)
    return T

def reorder(img, step, cut=False):
    # index length variables
    iLen, jLen = img.shape
    Length = iLen * jLen

    # arrays to store pixels of different types
    # upper left corner, upper right, lower left and lower right
    # respectively ll stores the most energy
    ll, lh, hl, hh = None, None, None, None
    
    # if it's matrix 2x2, iterate over every 2x2 blocks and store each into different array
    if step == 2:
        ll, lh, hl, hh = np.zeros(Length//4), np.zeros(Length//4), np.zeros(Length//4), np.zeros(Length//4)
        k = 0

        for i in range(0, iLen, 2):
            for j in range(0, jLen, 2):
                ll[k] = img[i,j]
                lh[k] = img[i,j+1]
                hl[k] = img[i+1,j]
                hh[k] = img[i+1,j+1]

                k+=1
        
        # give array of each type its appropriate form
        ll.shape, lh.shape, hl.shape, hh.shape = (iLen//2, jLen//2), (iLen//2, jLen//2), (iLen//2, jLen//2), (iLen//2, jLen//2)

    # for 4x4/8x8 matrices perform reordering recursively
    elif step == 4:
        ll, lh, hl, hh = reorder(img, 2, cut=True)
        ll = reorder(ll, 2)
        lh = reorder(lh, 2)
        hl = reorder(hl, 2)
        hh = reorder(hh, 2)

    elif step == 8:
        ll, lh, hl, hh = reorder(img, 4, cut=True)
        ll = reorder(ll, 2)
        lh = reorder(lh, 2)
        hl = reorder(hl, 2)
        hh = reorder(hh, 2)

    # allows return of unconcatennated arrays of different types
    if cut:
        return ll, lh, hl, hh
    
    # concatenate 4 arrays and return them back
    lllh = np.concatenate((ll, lh), axis=1)
    hlhh = np.concatenate((hl, hh), axis=1)
    return np.concatenate((lllh, hlhh), axis=0).astype(np.int32)

def haar_transform(img, bs):
    # get the matrix T depending on block size for haar transformation
    T = get_T(bs)

    # cast values in img to int32, otherwise range will be only uint8
    x = img.astype(np.int32)

    # declare result variable
    res = None

    # index length variables
    iLen, jLen = x.shape
    Length = iLen * jLen

    # if block size of 1x2 we perform 1d haar transformation and store 2 types of components
    # and reorder them here in place
    if bs == "1x2":
        x = x.flatten()
        ll, rr = np.zeros(Length//2), np.zeros(Length//2)
        k = 0
        for i in range(0, Length, 2):
            y = np.dot(T, np.array([x[i], x[i+1]]))

            ll[k], rr[k] = y[0], y[1]

            k+=1
        ll.shape, rr.shape = (iLen, jLen//2), (iLen, jLen//2)
        res = np.concatenate((ll,rr), axis=1).astype(np.int32)
    
    # for other block sizes, first perform haar transformation
    # then reorder the result with according step
    else:
        step = 0
        if bs == "2x2":
            step = 2
        elif bs == "4x4":
            step = 4
        elif bs == "8x8":
            step = 8
        
        # haar transformation
        for i in range(0, iLen, step):
            for j in range(0, jLen, step):
                # y = T*x*T.T
                y = np.dot(T, x[i:i+step, j:j+step])
                y = np.dot(y, T.T)

                # store it back to x, because well, space optimiztation?
                x[i:i+step, j:j+step] = y

        # reordering
        res = reorder(x, step)

    return res


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
        # entropy += p * np.log2(p)
    entropy *= (-1)

    return entropy


##############################################################################

# YCbCr components enumerator
Y, Cb, Cr = 0, 1, 2

# block sizes array
bs = ["1x2", "2x2", "4x4", "8x8"]

# quantization steps array
qs = [0, 2, 5, 10, 20, 50]

# load image
img_YCbCr = Image.open("../lena.png").convert("YCbCr")

# set the images as numpy array
img_asArray = np.array(img_YCbCr)

for block_size in bs:
    # plot 6 images as 2 rows, each 3 columns
    fig, axes = plt.subplots(2, 3)

    # visual improvement
    plt.subplots_adjust(hspace = 0.31)

    # counter for quantization step
    k = 0 

    # iterate over all axes, in .flatten (1d array) manner
    for i, ax in enumerate(axes.flat):
        # get only Y component
        result = img_asArray[:, :, Y]

        # perform haar transformation
        result = haar_transform(result, block_size)

        # perform quantization on Y component
        result = quantize(result, qs[k])

        # calculate entropy
        e = get_entropy(result)

        # count overall amount of pixels
        pixels = result.shape[0]*result.shape[1]

        # set labels on plot
        ax.text(-10, -10, "Quantization step = {0}".format(qs[k]))
        ax.set_xlabel("Entropy = {0:.4f}\nEstimated filesize = {1:.4f} KB".format(e, (e*pixels)/(8*1024)))

        # plot image
        ax.imshow(result, cmap='gray')

        k += 1

    # show plot for current quantization step
    plt.show()


