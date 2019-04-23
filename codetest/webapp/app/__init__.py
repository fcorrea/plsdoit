import os

from flask import Flask

from .config import DB_URI, SECRET_KEY
from .models import (
    db,
    Client,
    Priority,
    ProductArea,
    initialise_clients,
    initialise_priority,
    initialise_product_area,
)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = SECRET_KEY
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    if db.session.query(Client).count() == 0:
        initialise_clients()
    if db.session.query(Priority).count() == 0:
        initialise_priority()
    if db.session.query(ProductArea).count() == 0:
        initialise_product_area()
    return app
