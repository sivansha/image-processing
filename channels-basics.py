port cv2
from matplotlib import pyplot as plt

# images loaded using open cv2 and showed using matplotlib
bgr_img1 = cv2.imread('./lena.png')
bgr_img2 = cv2.imread('./northcap.png')

# images shown by mathplotlib
plt.imshow(bgr_img1, )
plt.title('Image loaded with open cv and showed with mathplotlib')
plt.show()
plt.imshow(bgr_img2)
plt.title('Image loaded with open cv and showed with mathplotlib')
plt.show()
# and the image is shown with red and blue hues switched.

# switch bgr --> grb and show again
rgb_img1 = cv2.cvtColor(bgr_img1, cv2.COLOR_BGR2RGB)
rgb_img2 = cv2.cvtColor(bgr_img2, cv2.COLOR_BGR2RGB)

# and indeed- the colors are correct.
plt.imshow(rgb_img1)
plt.title('results after swapping channel 1 and 3')
plt.show()
plt.imshow(rgb_img2)
plt.title('results after swapping channel 1 and 3')
plt.show()
