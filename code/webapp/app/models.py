from datetime import datetime

from sqlalchemy_utils import ChoiceType
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Client(Base):

    __tablename__ = "client"

    TYPES = [(1, u"Client A"), (2, u"Client B"), (3, u"Client C")]

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    type = Column(ChoiceType(TYPES))


class ProductArea(Base):

    __tablename__ = "product_area"

    TYPES = [(1, u"Policies"), (2, u"Billing"), (3, u"Claim"), (4, u"Reports")]

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    type = Column(ChoiceType(TYPES))


class FeatureRequest(Base):

    __tablename__ = "feature_request"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), unique=True, nullable=False, info={"label": "Title"})
    description = Column(Text(), nullable=False, info={"label": "Description"})
    target_date = Column(DateTime, nullable=False, info={"label": "Target Date"})
    client_priority = Column(Integer, nullable=False, info={"label": "Client Priority"})

    client_id = Column(Integer, ForeignKey(Client.id), nullable=False)
    client = relationship(Client, foreign_keys=[client_id])
    product_area_id = Column(Integer, ForeignKey(ProductArea.id), nullable=False)
    product_area = relationship(ProductArea, backref="feature_request")

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
