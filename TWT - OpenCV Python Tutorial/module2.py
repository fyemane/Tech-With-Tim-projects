import cv2
import random

img = cv2.imread('assets/logo.jpg', -1)

# opencv uses numpy
# loading image extract pixels into numpy array
print(img)
print(type(img))
# rows (height), columns (width), channels
# channels are color space
# 3 values that represent pixels, BGR between 0-255
print(img.shape)

# specific pixel
print(img[257][400])

# first 100 rows
for i in range(100):
    # each 100 rows, loop through entire width
    for j in range(img.shape[1]):
        # make each pixel random color
        img[i][j] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

# slice part of array into another array
tag = img[500:700, 600:900]
# location must have same dimensions and shape as array copied
img[100:300, 650:950] = tag

cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()