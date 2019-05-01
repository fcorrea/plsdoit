import os
from datetime import date

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
            target_date=date(2019, 5, 1),
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
        for priority in range(1, 4):
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
        result = (
            db.session.query(FeatureRequest)
            .filter(FeatureRequest.client_priority == 1)
            .one()
        )
        assert result.title == u"A new feature"
        # Lookup the existing feature request and check if it got its client_priority reset
        result = (
            db.session.query(FeatureRequest)
            .filter(FeatureRequest.client_priority == 2)
            .one()
        )
        assert result.client_priority == 2
        assert result.title == u"Feature with priority 1"

    def test_app_reorder_priorities_with_gap(self):
        self._makeOne(title=u"Feature with priority {}".format(1), client_priority=1)
        self._makeOne(title=u"Feature with priority {}".format(4), client_priority=4)
        self._makeOne(title=u"Feature with priority {}".format(5), client_priority=5)

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
        result = (
            db.session.query(FeatureRequest)
            .filter(FeatureRequest.client_priority == 1)
            .one()
        )
        assert result.title == u"A new feature"
        # client_priority 4 and 5 should not be affected as there's a gap
        result = (
            db.session.query(FeatureRequest)
            .filter(FeatureRequest.client_priority.in_((4, 5)))
            .all()
        )
        assert len(result) == 2
        assert result[0].title == u"Feature with priority 4"
        assert result[0].client_priority == 4
        assert result[1].title == u"Feature with priority 5"
        assert result[1].client_priority == 5
        result = (
            db.session.query(FeatureRequest)
            .filter(FeatureRequest.client_priority == 3)
            .count()
        )
        assert result == 0

    def test_app_delete_feature_request(self):
        self._makeOne()
        form_data = dict(feature_request_id=1)
        response = self.client.post("/delete", data=form_data)
        assert response.get_json() == {
            "status": "Successfully deleted new feature request"
        }
        result = db.session.query(FeatureRequest).count()
        assert result == 0

    def test_app_delete_feature_request_non_existing(self):
        self._makeOne()
        form_data = dict(feature_request_id=2)
        response = self.client.post("/delete", data=form_data)
        assert response.get_json() == {"status": "Could not delete feature request"}
        result = db.session.query(FeatureRequest).count()
        assert result == 1

    def test_app_edit_feature_request(self):
        self._makeOne()

        form_data = dict(
            feature_request_id=u"1",
            title=u"A new feature",
            description=u"A nice description changed",
            target_date=u"04/24/2019",
            client_id=u"1",
            client_priority=u"1",
            product_area_id=u"2",
            submit=True,
        )

        response = self.client.post("/edit", data=form_data)
        assert response.get_json() == {
            "status": "Successfully changed feature request."
        }
        result = db.session.query(FeatureRequest).one()
        assert result.description == u"A nice description changed"

    def test_app_edit_feature_request_change_priority(self):
        self._makeOne(title=u"Feature with priority {}".format(1), client_priority=1)
        self._makeOne(title=u"Feature with priority {}".format(2), client_priority=2)

        form_data = dict(
            feature_request_id=u"2",
            title=u"A new feature",
            description=u"A nice description changed",
            target_date=u"04/24/2019",
            client_id=u"1",
            client_priority=u"1",
            product_area_id=u"2",
            submit=True,
        )

        response = self.client.post("/edit", data=form_data)
        assert response.get_json() == {
            "status": "Successfully changed feature request. Client priority was reset."
        }
        # A reorder happened. The first FeatureRequest is now the second.
        result = (
            db.session.query(FeatureRequest)
            .filter(FeatureRequest.client_priority == 2)
            .one()
        )
        assert result.title == u"Feature with priority 1"
        assert FeatureRequest.query.get(2).client_priority == 1

    def test_app_list(self):
        self._makeOne(title=u"Feature with priority {}".format(1), client_priority=1)
        self._makeOne(title=u"Feature with priority {}".format(2), client_priority=2)

        response = self.client.post("/list")
        a_date = date(2019, 5, 1).strftime("%m/%d/%Y")
        expected = [
            {
                "client": "Client A",
                "client_priority": 1,
                "description": "A nice description",
                "id": 1,
                "product_area": "Billing",
                "target_date": a_date,
                "title": "Feature with priority 1",
            },
            {
                "client": "Client A",
                "client_priority": 2,
                "description": "A nice description",
                "id": 2,
                "product_area": "Billing",
                "target_date": a_date,
                "title": "Feature with priority 2",
            },
        ]
        assert response.get_json() == expected
