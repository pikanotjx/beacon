import cv2
import os
import numpy as np
from PIL import Image
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

cascade = cv2.CascadeClassifier(f"{BASE_DIR}/model.xml")
recognize = cv2.face.LBPHFaceRecognizer_create()


def get_data():
    current_id = 0
    label_id = {}
    face_train = []
    face_label = []

    faces = os.path.join(BASE_DIR, "faces")

    # Finds all the files in the `faces` directory
    for root, _, files in os.walk(faces):
        for file in files:

            # Reads in image (PNG or JPG) files for processing and training
            if file.endswith("png") or file.endswith("jpg"):
                image_path = os.path.join(root, file)

                # Chooses the label for the image to be the folder's name, which we assume to be the person's name
                label = os.path.basename(root).lower()

                # Assigning an ID to each label to be used by the recognizer
                if not label in label_id:
                    label_id[label] = current_id
                    current_id += 1
                id = label_id[label]

                # Converts the image into grayscale for processing by the recognizer
                pil_image = Image.open(image_path).convert("L")

                # Converts the image into a numpy array for processing by the recognizer
                image_array = np.array(pil_image, "uint8")

                # Runs the face detection algorithm on the image, returning a list of faces
                face = cascade.detectMultiScale(image_array)

                # Finds the face in the image and crops it out
                for x, y, w, h in face:
                    img = image_array[y:y+h, x:x+w]
                    cv2.imshow("Test", img)
                    cv2.waitKey(1)
                    face_train.append(img)
                    face_label.append(id)

    # Dumps the label_id dictionary into a pickle file for use by the recognizer
    with open("labels.pickle", "wb") as f:
        pickle.dump(label_id, f)

    return face_train, face_label


# Creates a recognizer and trains it with the data
face, ids = get_data()
recognize.train(face, np.array(ids))
recognize.save("trainer.yml")
