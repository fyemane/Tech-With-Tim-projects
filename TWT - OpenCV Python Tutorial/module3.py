import numpy as np
import cv2

# load a video capture image
# number of video capture device used
# if no cam, put video file into project, put file name instead
# takes hold of the camera
cap = cv2.VideoCapture(0)
# while loop until keyboard input, displays video camera
while True:
    # get a frame (image, numpy array) from video camera
    # ret is whether capture works properly
    ret, frame = cap.read()
    # get width and height of video capture
    # get 3 is width property, 4 is height
    width = int(cap.get(3))
    height = int(cap.get(4))

    # put 4 video frames together
    # create blank array to put face frame into
    # zero array with shape of frame, type of array values
    image = np.zeros(frame.shape, np.uint8)\
    # resize video frame
    smaller_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    # put smaller video frame into each corner
    # top left, bottom left, top right, bottom right
    image[:height//2, :width//2] = cv2.rotate(smaller_frame, cv2.ROTATE_180)
    image[height//2:, :width//2] = smaller_frame
    image[:height//2, width//2:] = cv2.rotate(smaller_frame, cv2.ROTATE_180)
    image[height//2:, width//2:] = smaller_frame

    # display frame
    cv2.imshow('frame', image)

    # wait 1 ms, then skip
    # if key pressed, will return ASCII value of key
    if cv2.waitKey(1) == ord('q'):
        break

# release the camera resource so another program can use it
cap.release()
cv2.destroyAllWindows()