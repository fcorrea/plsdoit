from datetime import datetime

import flask_sqlalchemy
from sqlalchemy_utils import ChoiceType

db = flask_sqlalchemy.SQLAlchemy()


class Client(db.Model):

    TYPES = [(1, u"Client A"), (2, u"Client B"), (3, u"Client C")]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(ChoiceType(TYPES))


class ProductArea(db.Model):

    TYPES = [(1, u"Policies"), (2, u"Billing"), (3, u"Claim"), (4, u"Reports")]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(ChoiceType(TYPES))


class FeatureRequest(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(
        db.String(200), unique=True, nullable=False, info={"label": "Title"}
    )
    description = db.Column(db.Text(), nullable=False, info={"label": "Description"})
    target_date = db.Column(db.DateTime, nullable=False, info={"label": "Target Date"})
    client_priority = db.Column(
        db.Integer, nullable=False, info={"label": "Client Priority"}
    )

    client_id = db.Column(db.Integer, db.ForeignKey(Client.id), nullable=False)
    client = db.relationship(Client, foreign_keys=[client_id])
    product_area_id = db.Column(
        db.Integer, db.ForeignKey(ProductArea.id), nullable=False
    )
    product_area = db.relationship(
        ProductArea, backref=db.backref("feature_request", lazy=True)
    )

    @property
    def serialize(self):
        """Create a serializable data strucutre"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "target_date": self.target_date.strftime("%m/%d/%Y"),
            "client": self.client.name,
            "product_area_id": self.product_area.id,
            "product_area_name": self.product_area.name,
            "client_priority": self.client_priority,
        }


def initialise_data():
    """Initialize database with default values"""
    if db.session.query(Client).count() == 0:
        initialise_clients()
    if db.session.query(ProductArea).count() == 0:
        initialise_product_area()


def initialise_clients():
    """Insert default Client data into the database"""
    default_clients = [u"Client A", u"Client B", u"Client C"]
    for name in default_clients:
        client = Client(name=name)
        db.session.add(client)
        db.session.commit()


def initialise_product_area():
    """Insert default ProductArea data into the database"""
    default_product_areas = [u"Policies", u"Billing", u"Claims", u"Reports"]
    for name in default_product_areas:
        product_area = ProductArea(name=name)
        db.session.add(product_area)
        db.session.commit()
