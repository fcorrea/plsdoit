import os
from datetime import datetime

from flask_testing import TestCase

from .. import create_app
from ..models import db, FeatureRequest


class TestFeatureRequestApp(TestCase):

    TESTING = True

    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _makeOne(self, title=None, client_priority=1):
        data = dict(
            title=title or u"A new feature",
            description=u"A nice description",
            target_date=datetime.now(),
            client_id=1,
            client_priority=client_priority,
            product_area_id=2,
        )
        feature_request = FeatureRequest(**data)
        db.session.add(feature_request)
        db.session.commit()

    def test_home(self):
        response = self.client.get("/")
        assert b"List of feature requests" in response.data
        assert b"Request New Feature" in response.data

    def test_app(self):
        form_data = dict(
            title=u"A new feature",
            description=u"A nice description",
            target_date=u"04/24/2019",
            client_id=u"1",
            client_priority=u"3",
            product_area_id=u"2",
            submit=True,
        )
        self.client.post("/new", data=form_data)
        result = db.session.query(FeatureRequest)
        assert result.count() == 1
        assert result.one().title == u"A new feature"

    def test_app_existing_title(self):
        self._makeOne()
        form_data = dict(
            title=u"A new feature",
            description=u"A nice description",
            target_date=u"04/24/2019",
            client_id=u"1",
            client_priority=u"3",
            product_area_id=u"2",
            submit=True,
        )
        response = self.client.post("/new", data=form_data)
        assert response.get_json() == {"title": ["Already exists."]}
        assert db.session.query(FeatureRequest).count() == 1

    def test_app_reorder_priorities(self):
        for priority in range(3):
            self._makeOne(
                title=u"Feature with priority {}".format(priority),
                client_priority=priority,
            )

        form_data = dict(
            title=u"A new feature",
            description=u"A nice description",
            target_date=u"04/24/2019",
            client_id=u"1",
            client_priority=u"1",
            product_area_id=u"2",
            submit=True,
        )
        self.client.post("/new", data=form_data)
        result = db.session.query(FeatureRequest).filter(
            FeatureRequest.client_priority == 1
        )
        assert result.count() == 1
        assert result.one().title == u"A new feature"
