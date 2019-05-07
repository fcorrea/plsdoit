import os
from datetime import date

from flask_testing import TestCase

from .. import create_app
from ..models import FeatureRequest
from ..app import get_features_counts_by_client, get_priority_counts
from ..database import init_db, db_session, Base, engine


class TestFeatureRequestApp(TestCase):

    TESTING = True

    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        return app

    def setUp(self):
        init_db()

    def tearDown(self):
        db_session.remove()
        Base.metadata.drop_all(engine)

    def _makeOne(self, title=None, client_id=1, client_priority=1):
        data = dict(
            title=title or u"A new feature",
            description=u"A nice description",
            target_date=date(2019, 5, 1),
            client_id=client_id,
            client_priority=client_priority,
            product_area_id=2,
        )
        feature_request = FeatureRequest(**data)
        db_session.add(feature_request)
        db_session.commit()

    def test_home(self):
        response = self.client.get("/")
        assert b"Feature Requests" in response.data
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
        result = db_session.query(FeatureRequest)
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
        assert db_session.query(FeatureRequest).count() == 1

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
            db_session.query(FeatureRequest)
            .filter(FeatureRequest.client_priority == 1)
            .one()
        )
        assert result.title == u"A new feature"
        # Lookup the existing feature request and check if it got its client_priority reset
        result = (
            db_session.query(FeatureRequest)
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
            db_session.query(FeatureRequest)
            .filter(FeatureRequest.client_priority == 1)
            .one()
        )
        assert result.title == u"A new feature"
        # client_priority 4 and 5 should not be affected as there's a gap
        result = (
            db_session.query(FeatureRequest)
            .filter(FeatureRequest.client_priority.in_((4, 5)))
            .all()
        )
        assert len(result) == 2
        assert result[0].title == u"Feature with priority 4"
        assert result[0].client_priority == 4
        assert result[1].title == u"Feature with priority 5"
        assert result[1].client_priority == 5
        result = (
            db_session.query(FeatureRequest)
            .filter(FeatureRequest.client_priority == 3)
            .count()
        )
        assert result == 0

    def test_app_delete_feature_request(self):
        self._makeOne()
        form_data = dict(id=1)
        response = self.client.post("/delete", data=form_data)
        assert response.get_json() == {
            "status": "Successfully deleted new feature request"
        }
        result = db_session.query(FeatureRequest).count()
        assert result == 0

    def test_app_delete_feature_request_non_existing(self):
        self._makeOne()
        form_data = dict(id=2)
        response = self.client.post("/delete", data=form_data)
        assert response.get_json() == {"status": "Could not delete feature request"}
        result = db_session.query(FeatureRequest).count()
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
        result = db_session.query(FeatureRequest).one()
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
            db_session.query(FeatureRequest)
            .filter(FeatureRequest.client_priority == 2)
            .one()
        )
        assert result.title == u"Feature with priority 1"
        assert FeatureRequest.query.get(2).client_priority == 1

    def test_app_list(self):
        for priority in range(1, 10):
            self._makeOne(
                title=u"Feature with priority {}".format(priority),
                client_priority=priority,
            )
        self._makeOne(
            title=u"Feature with priority 25", client_id=2, client_priority=25
        )

        response = self.client.get("/list")
        assert response.get_json()["total"] == 10

        form_data = dict(title=u"priority 9")
        response_data = self.client.get("/list", query_string=form_data).get_json()
        assert response_data["total"] == 1
        item = response_data["records"][0]
        assert "Feature with priority 9" == item["title"]

        form_data = dict(sortBy=u"title", direction=u"desc")
        response_data = self.client.get("/list", query_string=form_data).get_json()
        assert response_data["total"] == 10
        item = response_data["records"][0]
        assert "Feature with priority 9" == item["title"]

        form_data = dict(sortBy=u"client_priority", direction=u"desc")
        response_data = self.client.get("/list", query_string=form_data).get_json()
        assert response_data["total"] == 10
        item = response_data["records"][0]
        assert "Feature with priority 25" == item["title"]

        form_data = dict(sortBy=u"client", direction=u"desc")
        response_data = self.client.get("/list", query_string=form_data).get_json()
        assert response_data["total"] == 10
        item = response_data["records"][0]
        assert "Feature with priority 25" == item["title"]

        form_data = dict(limit=u"5", page=u"1")
        response_data = self.client.get("/list", query_string=form_data).get_json()
        assert response_data["total"] == 10
        assert len(response_data["records"]) == 5
        item = response_data["records"][0]
        assert "Feature with priority 1" == item["title"]

        form_data = dict(limit=u"5", page=u"2")
        response_data = self.client.get("/list", query_string=form_data).get_json()
        assert response_data["total"] == 10
        assert len(response_data["records"]) == 5
        item = response_data["records"][0]
        assert "Feature with priority 6" == item["title"]

    def test_feature_counts_by_client(self):
        self._makeOne(title=u"Feature with priority 1", client_priority=1)
        self._makeOne(title=u"Feature with priority 2", client_priority=2)
        self._makeOne(title=u"Feature with priority 3", client_priority=1, client_id=2)

        results = get_features_counts_by_client()
        assert results[0]["name"] == "Client A"
        assert results[0]["count"] == 2
        assert results[1]["name"] == "Client B"
        assert results[1]["count"] == 1

    def test_priority_counts(self):
        self._makeOne(title=u"Feature 1", client_priority=1)
        self._makeOne(title=u"Feature 2", client_priority=2)
        self._makeOne(title=u"Feature 3", client_priority=1, client_id=2)
        self._makeOne(title=u"Feature 4", client_priority=1, client_id=3)
        self._makeOne(title=u"Feature 5", client_priority=2, client_id=3)
        self._makeOne(title=u"Feature 6", client_priority=3, client_id=3)
        self._makeOne(title=u"Feature 7", client_priority=4, client_id=3)
        self._makeOne(title=u"Feature 8", client_priority=8, client_id=3)

        expected = [
            {"count": 3, "css_badge": "badge badge-danger count", "priority": 1},
            {"count": 2, "css_badge": "badge badge-danger count", "priority": 2},
            {"count": 1, "css_badge": "badge badge-danger count", "priority": 3},
            {"count": 1, "css_badge": "badge badge-info count", "priority": 4},
            {"count": 1, "css_badge": "badge badge-light count", "priority": 8},
        ]

        results = get_priority_counts()
        assert expected == results
