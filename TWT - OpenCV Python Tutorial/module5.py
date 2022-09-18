import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    # different color schemes: RGB, BGR, HSV
    # HSV - hue saturation and lightness/brightness
    # convert BGR to HSV
    # extracting color from image requires BGR2HSV conversion
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define colors to extract from image
    # pick lower and upper bound of colors to extract
    lower_blue = np.array([90, 50, 100])
    upper_blue = np.array([130, 255, 255])

    # mask is portion of image
    # returns mask of image of only blue images, other pixels blacked out
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # bitwise_and images together, mask as function to determine to keep pixel
    # 1 1 = 1
    # 0 1 = 0
    # 1 0 = 0
    # 0 0 = 0
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame', result)
    cv2.imshow('mask', mask)


    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# # insted of frame pass one pixel
# # cv2 expects image of shape, so pass 1 pixel image
# BGR_color = np.array([[[255, 0, 0]]])
# # gives array of HSV values
# x = cv2.cvtColor(BGR_color, cv2.COLOR_BGR2HSV)
