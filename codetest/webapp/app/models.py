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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


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
