import numpy as np
import cv2
# locate template image in base image
# images must be of similar size

# 0 for grayscale, many algs require grayscale iamges
img = cv2.resize(cv2.imread('assets/soccer_practice.jpg', 0), (0, 0), fx=0.8, fy=0.8)
template = cv2.resize(cv2.imread('assets/shoe.PNG', 0), (0, 0), fx=0.8, fy=0.8)
# height and width of template image - tuple (grayscale has no channel)
h, w = template.shape

# all diff methods of template matching, 6 main methods
# when starting template matching, use all methods, choose best one
methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED,
           cv2.TM_CCORR, cv2.TM_CCORR_NORMED,
           cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

# perform template matching using each method for comparison
for method in methods:
    # draw rect on new image
    img2 = img.copy()
    # perform template matching
    # perform convolution, slides images together to see how close a match
    # result is 2D array, how accurate a match in each image region
    # result of (W - w + 1, H - h + 1) (upper is base, lower is template)
    result = cv2.matchTemplate(img2, template, method)
    # find location of min/max vals
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # take top left location
    # take min value of sqdiff algs
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        location = min_loc
    else:
        location = max_loc

    # top left, bot rite corners
    # is tuple
    bottom_right = (location[0] + w, location[1] + h)
    cv2.rectangle(img2, location, bottom_right, 255, 5)

    cv2.imshow('Match', img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


"""
(3, 3)
W = 4
w = 2
H = 4
h = 2

[[255, 255, 255, 255],
 [255, 255, 255, 255],
 [255, 255, 255, 255],
 [255, 255, 255, 255]]

# slide template through base
[[255, 255],
 [255, 255]]

# output array, find max/min values
# reverse engineer position in base iamge
[[1, 1, 1],
 [1, 1, 1],
 [1, 1, 1]]
 """
