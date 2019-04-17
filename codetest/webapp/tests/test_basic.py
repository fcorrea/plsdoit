import os

from flask_testing import TestCase

from .. import create_app
from ..models import db


class BaseTest(TestCase):

    TESTING = True

    def create_app(self):

        # pass in test configuration
        return create_app()

    def setUp(self):

        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    def testFoo(self):
        assert os.environ["MYSQL_DB"] == 'Fooo'
