import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "db.sqlite"),
    )

    # Loads the instance config, if it exists, when not testing
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensures that the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Sets up the database and registers the close_db and init_db_command functions with the application instance
    from . import db
    db.init_app(app)

    return app
