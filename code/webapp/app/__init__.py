import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

from .app import features
from .config import SECRET_KEY
from .sample import load_sample_data

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = SECRET_KEY

    with app.app_context():
        app.register_blueprint(features)
        csrf.init_app(app)
        # app.app_context().push()
        Bootstrap(app)

        app.cli.add_command(load_sample_data)

        from .database import init_db, init_data

        init_db()
        init_data()

        return app
