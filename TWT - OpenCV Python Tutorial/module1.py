import cv2

# loading an image
# default mode in BGR color pattern
# load in grayscale, normal, w/o transparency
img = cv2.imread('assets/logo.jpg', 0)
# -1, cv2.IMGREAD_COLOR : loads a color image. Any transparency of image will be neglected. It is the default flag.
# 0, cv2.IMGREAD_GRAYSCALE : loads image in grayscale mode
# 1, cv2.IMGREAD_UNCHANGED : loads as such including alpha channel

# resize image by pixel or factor
img = cv2.resize(img, (400, 400))
img2 = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

# rotate image
img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

# save image
cv2.imwrite('new_img.jpg', img)

# displaying image
# create window with label name
cv2.imshow('Image', img)

# close the window
# wait x seconds then skips
# 0 is infinite, waits for keyboard input
cv2.waitKey(0)
cv2.destroyAllWindows()