from typing import Iterator

import pytest
from flask.testing import FlaskClient

from app import create_app
from models.base import Base
from utils import database

TEST_ACCOUNT = {
    "username": "testuser",
    "email": "kevgodev+test@gmail.com",
    "password": "testpassword",
    "confirm_password": "testpassword",
}


@pytest.fixture
def client() -> Iterator[FlaskClient]:
    app = create_app()
    with app.app_context():
        Base.metadata.drop_all(bind=database.get_engine())
        Base.metadata.create_all(bind=database.get_engine())
        with app.test_client() as client:
            yield client
