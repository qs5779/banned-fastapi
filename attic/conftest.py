"""Test module config for Aguda Flask application."""
import json
from http import HTTPStatus

import pytest
from aguada_flask import create_app
from aguada_flask.models import Cnames, Reserved, User, bcrypt, db
from shared import CNAME_SEED_DATA, CONTENT_TYPE, RESERVED_SEED_DATA


@pytest.fixture(scope="session")
def app():
    """Fixture to create the app."""
    return create_app({"TESTING": True})


@pytest.fixture(scope="session")
def _initdb(app):
    """Initialize the database with seed data."""
    pwhash = bcrypt.generate_password_hash("testing").decode("utf8")
    with app.app_context():
        db.session.add(User(username="tester", password=pwhash))
        for ipaddr, fdn in RESERVED_SEED_DATA.items():
            db.session.add(Reserved(addr=ipaddr, fqdn=fdn))
        for cnm, tgt in CNAME_SEED_DATA.items():
            db.session.add(Cnames(cname=cnm, target=tgt))
        db.session.commit()

        yield

        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="session")
def client(app, _initdb):
    """Create a test client."""
    return app.test_client()


@pytest.fixture(scope="session")
def post_access(client):
    """Fixture to create access headers."""
    response = client.post(
        "/api/v1/login",
        headers={"Content-Type": CONTENT_TYPE, "Accept": CONTENT_TYPE},
        data=json.dumps({"username": "tester", "password": "testing"}),
    )
    assert response.status_code < HTTPStatus.BAD_REQUEST
    assert response.is_json
    assert "access_token" in response.json
    access_token = response.json.get("access_token")
    return {
        "Authorization": "Bearer {0}".format(access_token),
        "Content-Type": CONTENT_TYPE,
        "Accept": CONTENT_TYPE,
    }


# @pytest.fixture(scope='module')
# def get_access(client):
#     """Fixture to create access headers."""
#     response = client.post(
#         "/v1/api/login",
#         headers={"Content-Type": CONTENT_TYPE, "Accept": CONTENT_TYPE},
#         data=json.dumps({"username": "tester", "password": "testing"}),
#     )
#     assert response.status_code < HTTPStatus.BAD_REQUEST
#     assert response.is_json
#     assert "access_token" in response.json
#     access_token = response.json.get("access_token")
#     return {
#         "Authorization": "Bearer {0}".format(access_token),
#         "Accept": CONTENT_TYPE,
#     }
