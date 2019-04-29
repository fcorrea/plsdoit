import os

from flask import Flask
from flask_bootstrap import Bootstrap

from .app import features
from .config import DB_URI, SECRET_KEY


def create_app():
    app = Flask(__name__)
    app.register_blueprint(features)
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = SECRET_KEY
    app.app_context().push()
    Bootstrap(app)

    from .models import db, initialise_data

    db.init_app(app)
    db.create_all()
    initialise_data()

    return app
