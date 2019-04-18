from datetime import datetime

import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class FeatureRequest(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    target_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    client = db.relationship(
        "Client", backref=db.backref("feature_requests", lazy=True)
    )
    client_priority_id = db.Column(
        db.Integer, db.ForeignKey("priority.id"), nullable=False
    )
    client_priority = db.relationship(
        "Priority", backref=db.backref("priority", lazy=True)
    )
    product_area_id = db.Column(
        db.Integer, db.ForeignKey("product_area.id"), nullable=False
    )
    product_area = db.relationship(
        "ProductArea", backref=db.backref("product_area", lazy=True)
    )


class Client(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


class Priority(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)


class ProductArea(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
