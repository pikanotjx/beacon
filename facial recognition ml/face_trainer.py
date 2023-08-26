import cv2
import os
import numpy as np
from PIL import Image
import pickle

cascade = cv2.CascadeClassifier("C:/Users/Tristan Sim/OneDrive/Documents/GitHub/sutdwasdoftime/facial recognition ml/haarcascade_frontalface_default.xml")

recognise = cv2.face.LBPHFaceRecognizer_create()

def traindata(name):

    face_dir = "C:/Users/Tristan Sim/OneDrive/Documents/GitHub/sutdwasdoftime/facial recognition ml/image_data/" + name
    current_id = 0
    label_id = {} #dictionanary
    face_train = [] # list
    face_label = [] # list

    # Finding all the folders and files inside the "image_data" folder
    for file in os.listdir(face_dir):
        filename = os.fsdecode(file)

        path = os.path.join(face_dir, file)
        # providing label ID as 1 or 2 and so on for different persons
        if not name in label_id:
            label_id[name] = current_id
            current_id += 1
        ID = label_id[name]
        # converting the image into gray scale image
        # you can also use cv2 library for this action
        pil_image = Image.open(path).convert("L")
        # converting the image data into numpy array
        image_array = np.array(pil_image, "uint8")

        # identifying the faces
        face = cascade.detectMultiScale(image_array)
        # finding the Region of Interest and appending the data
        for x,y,w,h in face:
            img = image_array[y:y+h, x:x+w]
        #image_array = cv2.rectangle(image_array,(x,y),(x+w,y+h),(255,255,255),3)
            cv2.imshow("Test",img)
            cv2.waitKey(1)
            face_train.append(img)
            face_label.append(ID)

  # string the labels data into a file
    with open("labels.pickle", 'wb') as f:
        pickle.dump(label_id, f)
   

    return face_train,face_label

# creating ".yml" file
name = "Jeremy"
face,ids = traindata(name)

recognise.train(face, np.array(ids))
recognise.save(name + "_trainer.yml")  