import logging

from flask import session
from flask.testing import FlaskClient
from werkzeug.wrappers import Response

TEST_ACCOUNT = {
    "username": "testuser",
    "email": "kevgodev+test@gmail.com",
    "password": "testpassword",
    "confirm_password": "testpassword",
}


# Utils
def create_test_user(client: FlaskClient) -> Response:
    return client.post("/api/auth/register", json=TEST_ACCOUNT)


def login_test_user(client: FlaskClient) -> Response:
    return client.post(
        "/api/auth/login",
        json={
            "username": TEST_ACCOUNT["username"],
            "password": TEST_ACCOUNT["password"],
        },
    )


def logout_test_user(client: FlaskClient) -> Response:
    return client.post("/api/auth/logout")


def test_create_user(client: FlaskClient):
    response = create_test_user(client)
    logging.info(f"create_user response: {response.text}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] == True
    assert "id" in data["data"]["user"]
    assert data["data"]["user"]["username"] == TEST_ACCOUNT["username"]
    assert data["data"]["user"]["email"] == TEST_ACCOUNT["email"]


def test_login(client: FlaskClient):
    # Create user first
    assert create_test_user(client).status_code == 200
    # test login
    response = client.post(
        "/api/auth/login",
        json={
            "username": TEST_ACCOUNT["username"],
            "password": TEST_ACCOUNT["password"],
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"]
    assert "id" in data["data"]["user"]
    assert data["data"]["user"]["username"] == TEST_ACCOUNT["username"]
    assert data["data"]["user"]["email"] == TEST_ACCOUNT["email"]
    assert "user_id" in session
    assert session["user_id"] == data["data"]["user"]["id"]
    assert "username" in session
    assert session["username"] == data["data"]["user"]["username"]


def test_logout(client: FlaskClient):
    # Create user and login first
    assert create_test_user(client).status_code == 200
    assert login_test_user(client).status_code == 200
    # test logout
    response = client.get("/api/auth/logout")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"]
    assert "user_id" not in session
    assert "username" not in session


def test_me(client: FlaskClient):
    assert create_test_user(client).status_code == 200
    assert login_test_user(client).status_code == 200
    # Test me endpoint with a user
    response = client.get("/api/auth/me")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"]
    assert data["data"]["user"]["id"] == session["user_id"]
    assert data["data"]["user"]["username"] == session["username"]
    assert data["data"]["user"]["email"] == TEST_ACCOUNT["email"]
    # Test me endpoint after logout
    assert logout_test_user(client).status_code == 200
    response = client.get("/api/auth/me")
    assert response.status_code == 400
