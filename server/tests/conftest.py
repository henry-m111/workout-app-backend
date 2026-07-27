import pytest

from app import create_app
from models import db


@pytest.fixture
def app():
    test_app = create_app("sqlite:///:memory:")
    test_app.config["TESTING"] = True

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
