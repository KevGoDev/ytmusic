from flask.testing import FlaskClient


def test_status(client: FlaskClient):
    # login first
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json["data"]["status"] == "ok"
