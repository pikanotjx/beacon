import cv2
import pickle##
import serial

# Setting serial port to COM4 at bard rate of 9600
port = serial.Serial('COM3',9600)

video = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier("C:/Users/Tristan Sim/OneDrive/Documents/GitHub/sutdwasdoftime/facial recognition ml/haarcascade_frontalface_default.xml")

recognise = cv2.face.LBPHFaceRecognizer_create()
recognise.read("C:/Users/Tristan Sim/OneDrive/Documents/GitHub/sutdwasdoftime/facial recognition ml/trainer.yml")

labels = {}
with open("C:/Users/Tristan Sim/OneDrive/Documents/GitHub/sutdwasdoftime/facial recognition ml/labels.pickle", 'rb') as f:
    og_label = pickle.load(f)
    labels = {v:k for k,v in og_label.items()}
    print(labels)



while True:
    check,frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face = cascade.detectMultiScale(gray, scaleFactor = 1.05, minNeighbors = 5)
    #print(face)

    for x,y,w,h in face:
        face_save = gray[y:y+h, x:x+w]

        ID, conf = recognise.predict(face_save)
        #print(ID,conf)
        if conf >= 20 and conf <= 115:
            print(ID)
            print(labels[ID])
            cv2.putText(frame,labels[ID],(x-10,y-10),cv2.FONT_HERSHEY_COMPLEX ,1, (18,5,255), 2, cv2.LINE_AA )
    
        if labels[ID] == "tristan":
            port.write(b'1')
        else:
            port.write(b'0')





    cv2.imshow("Video",frame)
    key = cv2.waitKey(1)
    if(key == ord('q')):
        break

video.release()
cv2.destroyAllWindows()
