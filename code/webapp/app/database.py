from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import DB_URI

engine = create_engine(DB_URI, convert_unicode=True, echo=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from .models import Client, ProductArea, FeatureRequest

    Base.metadata.create_all(bind=engine)


def init_data():
    from .models import Client, ProductArea

    if db_session.query(Client).count() == 0:
        default_clients = [u"Client A", u"Client B", u"Client C"]
        for name in default_clients:
            client = Client(name=name)
            db_session.add(client)

    if db_session.query(ProductArea).count() == 0:
        default_product_areas = [u"Policies", u"Billing", u"Claims", u"Reports"]
        for name in default_product_areas:
            product_area = ProductArea(name=name)
            db_session.add(product_area)

    db_session.commit()
