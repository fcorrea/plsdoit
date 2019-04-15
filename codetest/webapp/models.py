import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class FeatureRequest(db.Model):
    __tablename__ = 'featurerequest'
    id = db.Column(db.Integer, primary_key=True)
