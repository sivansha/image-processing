from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

R, G, B = 0, 1, 2

# load image
img1 = Image.open("../lena.png")

# TASK A: show the R, G, B components
# set the image as numpy array
img1_asArray = np.array(img1)

# recreate and show image as black and white image
Image.fromarray(img1_asArray[:, :, R], "L").show()
Image.fromarray(img1_asArray[:, :, G], "L").show()
Image.fromarray(img1_asArray[:, :, B], "L").show()

# TASK B: show the R, G, B distribution
# calculate histogram
hist = img1.histogram()

# plot R, G, and B distribution
plt.plot(hist[0:256],   color='R', label="Red")
plt.plot(hist[256:512], color='G', label="Green")
plt.plot(hist[512:768],   color='B', label="Blue")
plt.legend(loc='upper left')
plt.title('distributions of RGB component’s intensities')
plt.ylabel('Pixels')
plt.xlabel('RGB values')
plt.show()
