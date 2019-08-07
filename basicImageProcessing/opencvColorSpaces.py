import cv2

# by counting the flags we will get all the supported color spaces.
flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
print(len(flags))
