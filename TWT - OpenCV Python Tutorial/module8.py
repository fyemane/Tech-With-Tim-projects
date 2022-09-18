import cv2

cap = cv2.VideoCapture(0)
# haar cascades = pre-trained classifier which is an algorithm looking for features
# face cascade is classifier looking for face features
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# looking for eye features
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # face cascade returns all locations of faces
    # scale factor shrinks image for haarcascade to analyze at each iteration
    # 1.05 is good factor, high value -> fast detection, low accuracy
    # minNeighbors is how many neighbors overlapping in area to determine face
    # 3-6, affects quality of detections, high value -> less detection, higher quality
    # minSize - min rect size, maxSize - max rect size

    # find all faces in frame
    faces = face_cascade.detectMultiScale(gray, 1.5, 5)

    # draw rect around faces from cascade
    for (x, y, w, h) in faces:
        # (x, y) is top left corner
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)

        # find area of image that covers his face, use to find eyes
        # pass face image to eye classifier to look for eyes
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # look for eyes
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)

        # draw rect around eyes
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
