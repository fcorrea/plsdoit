from datetime import datetime

import flask_sqlalchemy
from sqlalchemy_utils import ChoiceType

db = flask_sqlalchemy.SQLAlchemy()


class Client(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


class Priority(db.Model):

    PRIORITIES = [(1, u"Very High"), (2, u"High"), (3, u"Medium"), (4, u"Low")]

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(ChoiceType(PRIORITIES))


class ProductArea(db.Model):

    AREAS = [(1, u"Policies"), (2, u"Billing"), (3, u"Claim"), (4, u"Reports")]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(ChoiceType(AREAS))


class FeatureRequest(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(
        db.String(200), unique=True, nullable=False, info={"label": "Title"}
    )
    description = db.Column(db.Text(), nullable=False, info={"label": "Description"})
    target_date = db.Column(db.DateTime, nullable=False, info={"label": "Target Date"})

    client_id = db.Column(db.Integer, db.ForeignKey(Client.id), nullable=False)
    client = db.relationship(Client, backref=db.backref("feature_request", lazy=True))
    client_priority_id = db.Column(
        db.Integer, db.ForeignKey(Priority.id), nullable=False
    )
    client_priority = db.relationship(
        Priority, backref=db.backref("priority", lazy=True)
    )
    product_area_id = db.Column(
        db.Integer, db.ForeignKey(ProductArea.id), nullable=False
    )
    product_area = db.relationship(
        ProductArea, backref=db.backref("product_area", lazy=True)
    )


def initialise_data():
    """Initialize database with default values"""
    if db.session.query(Client).count() == 0:
        initialise_clients()
    if db.session.query(Priority).count() == 0:
        initialise_priority()
    if db.session.query(ProductArea).count() == 0:
        initialise_product_area()


def initialise_clients():
    """Insert default Client data into the database"""
    default_clients = [u"Client A", u"Client B", u"Client C"]
    for name in default_clients:
        client = Client(name=name)
        db.session.add(client)
        db.session.commit()


def initialise_priority():
    """Insert default Priority data into the database"""
    default_priorities = [1, 2, 3, 4]
    for value in default_priorities:
        priority = Priority(value=value)
        db.session.add(priority)
        db.session.commit()


def initialise_product_area():
    """Insert default ProductArea data into the database"""
    default_product_areas = [u"Policies", u"Billing", u"Claims", u"Reports"]
    for name in default_product_areas:
        product_area = ProductArea(name=name)
        db.session.add(product_area)
        db.session.commit()
