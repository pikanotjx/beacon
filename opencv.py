import cv2

video = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier("C:/Users/Tristan Sim/Study Folder/SUTD WTH/opencv/haarcascade_frontalface_default.xml")

while True:
    check, frame = video.read()

    face = cascade.detectMultiScale(frame, scaleFactor = 1.1, minNeighbors = 6)

    for x,y,w,h in face:
        frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,255), 3)

    cv2.imshow("Video", frame)

    if (cv2.waitKey(1) == ord('q')):
        break