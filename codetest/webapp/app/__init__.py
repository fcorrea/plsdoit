import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

from .app import features
from .config import DB_URI, SECRET_KEY
from .sample import load_sample_data

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    csrf.init_app(app)
    app.register_blueprint(features)
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = SECRET_KEY
    app.app_context().push()
    Bootstrap(app)

    app.cli.add_command(load_sample_data)

    from .models import db, initialise_data

    db.init_app(app)
    db.create_all()
    initialise_data()

    return app
