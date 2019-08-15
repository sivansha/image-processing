#!/usr/bin/env python3
# -*- coding: utf-8 -*

from PIL import Image
import numpy as np
import os
from q5_a import *
from matplotlib import pyplot as plt

def main():
    debug=False

    images = [b"lena.png", b"northcap.png"]
    #dict with key quality and values [file_size,psnr]


    for img in images:
        quality_res = []
        img_YCbCr = Image.open(b"../"+img).convert("YCbCr")
        if debug:
            img_YCbCr.show()

        img_asArray = np.array(img_YCbCr)

        for i in range(100,0,-10):
            filename = b"../images/q5/q5_b_"+img+b"_quality_"+bytes(str(i),"ascii")+b".jpeg"
            if debug:
                print(filename)
                print(i)

            img_YCbCr.save(filename,'JPEG',quality=i)
            quality_res.append([i,os.path.getsize(filename),calc_psnr(b"../"+img, filename)])

        if debug:
            print(quality_res)

        plot_res(quality_res)

def plot_res(quality_res, optimization = 'False'):
    N = len(quality_res)
    filesizes = [x[1]/1024 for x in quality_res]
    psnrs = [x[2] for x in quality_res]

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()

    ax.set_ylabel('File size [KByte]')
    ax.yaxis.label.set_color('blue')
    ax.plot(ind, filesizes,'b-', linewidth=2.0)
    if filesizes[0] > 1000:
        ax.set_ylim([0, 11700])
    else:
        ax.set_ylim([0, 230])

    

    ax2 = ax.twinx()
    ax2.bar(ind, psnrs, width, alpha=0.4, color='r')
    # add some text for labels, title and axes ticks
    ax2.set_ylabel('PSNR [dB]')
    ax2.yaxis.label.set_color('red')
    ax2.set_title('JPEG Compression, Opimization = '+optimization)
    ax2.set_xticks(ind)
    ax2.set_xticklabels([x[0] for x in quality_res])
    ax2.set_xlabel('Quality [%]')
    ax2.set_ylim([0,60])

    #second y axis


    plt.show()

if __name__ == "__main__":
    main()
