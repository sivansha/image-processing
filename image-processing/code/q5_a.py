#!/usr/bin/env python3
# -*- coding: utf-8 -*

from PIL import Image
import numpy as np

def calc_psnr(img1, img2, debug=False):
    '''
    Function to calculate the peak signal-to-noise-ratio between to given images.
    :param img: takes the path of an image as a string
    :param debug: optional debug switch, which can be set to True, to see additional output
    :return: return the peak signal to noise ratio of the given images Y-channels
    '''
    y_plane=0
    R=255

    if img1==img2:
        print("Please supply two different pictures.")
        return

    #load images and save as arrays
    img1_YCbCr = Image.open(img1).convert("YCbCr")
    img1_asArray = np.array(img1_YCbCr)

    img2_YCbCr = Image.open(img2).convert("YCbCr")
    img2_asArray = np.array(img2_YCbCr)
    
    if debug:
        #show images
        img1_Y = Image.fromarray(img2_asArray[:, :, y_plane], "L")
        img2_Y=Image.fromarray(img1_asArray[:, :, y_plane], "L")
        img1_Y.show()
        img2_Y.show()

    #calculate psnr
    mse=calc_mse(img1_asArray[:, :, y_plane],img2_asArray[:, :, y_plane],debug)
    return 10*np.log10(R*R/mse)

def calc_mse(array1,array2, debug=False):
    '''
    Function to calculate the mean squared error of two arrays
    :param array1: the first array to be use for the mean error calculation, must be of same size as array2
    :param array2: the first array to be use for the mean error calculation, must be of same size as array1
    :param debug: optional debug switch, which can be set to True, to see additional output
    :return: mean squared error between the two given arrays
    '''
    if debug:
        print(array1)
        print(array2)
    return np.sum(np.square(array1-array2))/array1.size
