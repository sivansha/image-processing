import cv2
import numpy as np

# max window size for mean convolution
max_win_size = 11

# load image and convert it to YUV:
bgr_img1 = cv2.imread('./lena.png')
yuv_img1 = cv2.cvtColor(bgr_img1, cv2.COLOR_BGR2YUV)
# extract the Y channel:
yuv_img1_asArray = np.array(yuv_img1)
y_img_as_array = yuv_img1_asArray[:, :, 0]

# perform median consolation and store the results from n = [3, max_win_size)
for i, n in enumerate(range(100, 101)):
    # average value of n*n window
    kernel = np.ones((n, n))/(n*n)
    # the n*n window "slides" and each pixel in turn is in the middle of the window, and it's assigned the average of the window:
    y_img_convoluted = cv2.filter2D(y_img_as_array, -1, kernel)
    numpy_horizontal = np.hstack((y_img_as_array, y_img_convoluted))
    cv2.imshow("mean convolution n=" + str(n), numpy_horizontal)
    cv2.waitKey(0)
    cv2.imwrite("./images/=" + str(n) + '.png', numpy_horizontal)
