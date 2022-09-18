import numpy as np
import cv2

img = cv2.imread('assets/chessboard.png')
img = cv2.resize(img, (0, 0), fx=0.75, fy=0.75)
# before detecting edges, convert to grayscale
# algs work on grayscale easier
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# corner detection algorithm
# returns N best corners from image alg detects
# minimum quality is 0-1 (1 is perfect, 0 no confidence)
# min Euclidean distance btwn 2 corners = sqrt((x2 - x1)^2 + (y2 - y1)^2)
corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
# convert corners to integers
corners = np.int0(corners)

# loop through corners
for corner in corners:
    # flatten array by removing interior arrays, puts into tuple
    x, y = corner.ravel()
    cv2.circle(img, (x, y), 5, (255, 0, 0), -1)

# loops through all corners
for i in range(len(corners)):
    # loop through all corne rs not looped through
    for j in range(i + 1, len(corners)):
        # pair of corners
        corner1 = tuple(corners[i][0])
        corner2 = tuple(corners[j][0])
        # generates 3 random colors
        # returns list of 32/64 bit int, need 8 bit
        # map function to values, returns new array with function resuls
        # anonymous Lambda function to convert to 8bit ints
        # puts 3 ints into tuple
        color = tuple(map(lambda x: int(x), np.random.randint(0, 255, size=3)))
        # join line btwn corners
        cv2.line(img, corner1, corner2, color, 1)

cv2.imshow('Frame', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
