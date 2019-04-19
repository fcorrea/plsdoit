import os

from flask import Flask

from .config import DB_URI, SECRET_KEY
from .models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    return app
