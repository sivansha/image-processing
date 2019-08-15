from matplotlib import pyplot as plt
from scipy import fftpack
from PIL import Image
import numpy as np

def quantize(img, step):
    if step != 0:
        # take every entry in matrix and perform a whole number division on every element by the number of steps
        # multiply again to receive the floor value for each entry 
        return (img // step) * step
    else:
        return img

def reorder(img, step, cut=False):
    iLen, jLen = img.shape
    Length = iLen * jLen
    ll, lh, hl, hh = None, None, None, None
    
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
        
        ll.shape, lh.shape, hl.shape, hh.shape = (iLen//2, jLen//2), (iLen//2, jLen//2), (iLen//2, jLen//2), (iLen//2, jLen//2)

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

    if cut:
        return ll, lh, hl, hh
    lllh = np.concatenate((ll, lh), axis=1)
    hlhh = np.concatenate((hl, hh), axis=1)
    return np.concatenate((lllh, hlhh), axis=0).astype(np.int32)


def dct_transform(img, bs):

    x = img.astype(np.int32)
    res = None
    iLen, jLen = x.shape
    Length = iLen * jLen

    if bs == "1x2":
        x = x.flatten()
        ll, rr = np.zeros(Length//2), np.zeros(Length//2)
        k = 0
        for i in range(0, Length, 2):
            y = fftpack.dct(np.array([x[i], x[i+1]]))

            ll[k], rr[k] = y[0], y[1]

            k+=1
        ll.shape, rr.shape = (iLen, jLen//2), (iLen, jLen//2)
        res = np.concatenate((ll,rr), axis=1).astype(np.int32)

    else:
        step = 0
        if bs == "2x2":
            step = 2
        elif bs == "4x4":
            step = 4
        elif bs == "8x8":
            step = 8
        
        # dct transformation
        for i in range(0, iLen, step):
            for j in range(0, jLen, step):
                y = fftpack.dctn(x[i:i+step, j:j+step])
                
                x[i:i+step, j:j+step] = y

        # reordering
        res = reorder(x, step)
                
    return res
    # return np.rint(y).astype(int)

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

bs = ["1x2", "2x2", "4x4", "8x8"]
qs = [0, 2, 5, 10, 20, 50]

# load image
img_YCbCr = Image.open("../lena.png").convert("YCbCr")

# set the images as numpy array
img_asArray = np.array(img_YCbCr)

for block_size in bs:
    fig, axes = plt.subplots(2, 3)
    plt.subplots_adjust(hspace=0.31)
    k = 0 

    for i, ax in enumerate(axes.flat):
        result = img_asArray[:, :, Y]

        result = dct_transform(result, block_size)

        result = quantize(result, qs[k])

        e = get_entropy(result)
        pixels = result.shape[0]*result.shape[1]

        ax.text(-10, -10, "Quantization step = {0}".format(qs[k]))
        ax.set_xlabel("Entropy = {0:.4f}\nEstimated filesize = {1:.4f} KB".format(e, (e*pixels)/(8*1024)))

        ax.imshow(result, cmap='gray')

        k += 1

    plt.show()


