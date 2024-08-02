from jose import jwt
from .config import *


def test_user_registration(client):
    response = client.post(
        "/users/",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
        },
    )
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"


def test_user_registration_missing_field(client):
    response = client.post(
        "/users/", json={"username": "newuser", "password": "newpassword"}
    )
    assert response.status_code == 422  # Unprocessable Entity


def test_user_login(client, test_user):
    response = client.post(
        "/token", data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_invalid_user_login(client):
    response = client.post(
        "/token", data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_login_missing_field(client):
    response = client.post("/token", data={"username": "testuser"})
    assert response.status_code == 422  # Unprocessable Entity


def test_jwt_token(client, token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "testuser"


def test_invalid_jwt_token(client, token):
    invalid_token = token + "invalid"
    response = client.get(
        "/todos/", headers={"Authorization": f"Bearer {invalid_token}"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
