import cv2
import pickle
import serial
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PORT = "COM3"  # Change this to the port that your Arduino is connected to
port = serial.Serial(PORT, 9600)

# Loads the trained recognizer
video = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier(f"{BASE_DIR}/model.xml")
recognize = cv2.face.LBPHFaceRecognizer_create()
recognize.read(f"{BASE_DIR}/trainer.yml")

labels = {}
with open(f"{BASE_DIR}/labels.pickle", "rb") as file:
    saved_labels = pickle.load(file)
    labels = {value: key for key, value in saved_labels.items()}
    print(labels)

while True:
    # Reads in the video feed, converts it to grayscale, and runs the face detection algorithm
    check, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5)

    faces = []

    for x, y, w, h in face:
        face_save = gray[y:y+h, x:x+w]

        # Uses the trained recognizer to predict the ID of the face
        id, confidence = recognize.predict(face_save)
        # Sets the confidence threshold for the recognizer to consider a prediction valid
        if confidence >= 20 and confidence <= 115:
            faces.append(labels[id])
            print(id)
            print(labels[id])
            cv2.putText(frame, labels[id], (x-10, y-10),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (18, 5, 255), 2, cv2.LINE_AA)

    # Sends a signal to the Arduino to turn on the LED if the face is recognized as Tristan
    # TODO: Make this dynamic
    if "tristan sim".lower() in faces:
        port.write(b"1")
    else:
        port.write(b"0")

    # Displays the video feed and waits for the user to press "q" to quit
    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)
    if (key == ord("q")):
        break

# Releases the video feed and closes all windows
video.release()
cv2.destroyAllWindows()
