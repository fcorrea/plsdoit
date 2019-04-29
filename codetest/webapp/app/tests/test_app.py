import os

from flask_testing import TestCase

from .. import create_app
from ..models import db, FeatureRequest


class TestFeatureRequestApp(TestCase):

    TESTING = True

    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home(self):
        response = self.client.get("/")
        assert b"List of feature requests" in response.data
        assert b"Request New Feature" in response.data

    def test_form(self):
        form_data = dict(
            title=u"A new feature",
            description=u"A nice description",
            target_date=u"04/24/2019",
            client_id=u"1",
            client_priority_id=u"3",
            product_area_id=u"2",
            submit=True,
        )
        self.client.post("/new", data=form_data)
        result = db.session.query(FeatureRequest)
        assert result.count() == 1
        assert result.one().title == u"A new feature"
