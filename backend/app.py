from flask import (Flask, render_template, request, abort, redirect, url_for)
from werkzeug.exceptions import BadRequest
from vertexai.preview.language_models import TextGenerationModel
from google.cloud import aiplatform
from .db import get_db

app = Flask(__name__)
aiplatform.init(project="sandbox-394407")


@app.route("/people")
def list_people():
    # Gets the list of saved people from the database
    db = get_db()
    people = db.execute("SELECT * FROM person").fetchall()

    return render_template("people.html", people=people)


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
            f"Generate an integer between 0 and 255 describing how bright an LED should be for the given description of a user's light preference: {preference}", **parameters)
        print(response)

        try:
            db.execute(
                "INSERT INTO person (personName, lightPreference, lightDescription) VALUES (?, ?, ?)", (name, int(response.text), preference))
            db.commit()
        except db.IntegrityError:
            abort(400)
        else:
            return redirect(url_for("list_people"))


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return "Please provide a name and preference", 400
