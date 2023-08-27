from flask import (Flask, render_template, request,
                   abort, redirect, url_for, Response)
from werkzeug.exceptions import BadRequest
from vertexai.preview.language_models import TextGenerationModel
from google.cloud import aiplatform
from .db import get_db
import cv2
import os
import uuid
import pickle

app = Flask(__name__)
aiplatform.init(project="sandbox-394407")


@app.route("/people")
def list_people():
    # Gets the list of saved people from the database
    db = get_db()
    people = db.execute("SELECT * FROM person").fetchall()

    return render_template("people.html", people=people)


def capture_frame(name):
    cap = cv2.VideoCapture(0)
    frames = []
    frame_count = 0
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        if len(frames) == 50:
            cap.release()
            break

        frame_count += 1
        if frame_count % 10 == 0:
            frame_count = 0
            frames.append(frame)
            print(f"Captured frame {len(frames)}")

        # Display the resulting frame
        # Encodes the captured frame as a JPEG
        ret, buffer = cv2.imencode(".jpg", frame)
        # Yields the frame as a multipart response
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

    person_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ml", "faces", name)

    if not os.path.exists(person_path):
        os.makedirs(person_path)
    for frame in frames:
        image_path = os.path.join(person_path, f"{name}.{str(uuid.uuid1())}.jpg")
        cv2.imwrite(image_path, frame)


@app.route("/capture_face/<name>")
def capture_face(name):
    return Response(capture_frame(name), mimetype="multipart/x-mixed-replace; boundary=frame")


def display_camera():
    video = cv2.VideoCapture(0)
    ML_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ml")
    cascade = cv2.CascadeClassifier(os.path.join(ML_DIR, "model.xml"))
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(os.path.join(ML_DIR, "trainer.yml"))

    labels = {}
    with open(os.path.join(ML_DIR, "labels.pickle"), "rb") as file:
        labels = {value: key for key, value in pickle.load(file).items()}
        print(labels)
    
    preferences = {}
    with app.app_context():
        db = get_db()
        for person in db.execute("SELECT * FROM person").fetchall():
            preferences[person["personName"].lower()] = str(round(int(person["lightPreference"]) / 255 * 100)) + "%"
        print(preferences)

    while True:
        # Reads in the video feed, converts it to grayscale, and runs the face detection algorithm
        check, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5)

        for x, y, w, h in face:
            face_save = gray[y:y+h, x:x+w]

            # Uses the trained recognizer to predict the ID of the face
            id, confidence = recognizer.predict(face_save)

            # Sets the confidence threshold for the recognizer to consider a prediction valid
            if confidence >= 20 and confidence <= 115:
                print(id)
                print(labels[id])
                cv2.putText(frame, labels[id] + " " + preferences[labels[id]], (x-10, y-10),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (18, 5, 255), 2, cv2.LINE_AA)
                
            key = cv2.waitKey(1)
            if (key == ord("q")):
                # Releases the video feed and closes all windows
                video.release()
                break
                
            # Display the resulting frame
            # Encodes the captured frame as a JPEG
            ret, buffer = cv2.imencode(".jpg", frame)
            # Yields the frame as a multipart response
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

        # Displays the video feed and waits for the user to press "q" to quit
        # cv2.imshow("Video", frame)

@app.route("/recognize")
def recognize():
    return render_template("recognize.html")

@app.route("/recognize_faces")
def recognize_faces():
    return Response(display_camera(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/setup/<name>")
def setup(name="Unknown"):
    return render_template("setup.html", name=name)

@app.route("/people/create", methods=["POST"])
def create_person():
    print(request.form)
    name = request.form["name"]
    preference = request.form["preferences"]

    if not name or not preference:
        abort(400)
    else:
        db = get_db()

        # Uses the TextGenerationModel to come up with an appropriate brightness value
        parameters = {
            "temperature": 0,
        }
        model = TextGenerationModel.from_pretrained("text-bison@001")
        response = model.predict(
            f"Generate an integer between 0 and 255 describing how bright an LED should be for the given description of a user's light preference: \"{preference}\" Only give an integer, and do not give anything else.", **parameters)
        print(response)

        try:
            db.execute(
                "INSERT INTO person (personName, lightPreference, lightDescription) VALUES (?, ?, ?)", (name, int(response.text), preference))
            db.commit()
        except db.IntegrityError:
            abort(400)
        else:
            return redirect(url_for("setup", name=name))


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return "Please provide a name and preference", 400
