#!/usr/bin/env python3
# -*- coding: utf-8 -*

from PIL import Image
import numpy as np
import os
from q5_b import *

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

        for i in range(100, 0, -10):
            filename = b"../images/q5/q5_b_"+img+b"_quality_"+bytes(str(i),"ascii")+b"_optimized.jpeg"
            if debug:
                print(filename)
                print(i)

            img_YCbCr.save(filename,'JPEG',quality=i,optimize=True)
            quality_res.append([i, os.path.getsize(filename), calc_psnr(b"../"+img, filename)])

        if debug:
            print(quality_res)

        plot_res(quality_res, 'True')


if __name__ == "__main__":
    main()
