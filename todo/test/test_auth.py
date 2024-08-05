from jose import jwt, JWTError
from .config import *


def test_user_registration_missing_field():
    response = client.post(
        "/users/", json={"username": "newuser", "password": "newpassword"}
    )
    assert response.status_code == 422  # Unprocessable Entity


def test_user_registration():
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


def test_invalid_user_login():
    response = client.post(
        "/token", data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_login_missing_field():
    response = client.post("/token", data={"username": "testuser"})
    assert response.status_code == 422  # Unprocessable Entity


def test_user_login(test_user):
    response = client.post(
        "/token", data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_invalid_jwt_token(token):
    invalid_token = token + "invalid"
    with pytest.raises(JWTError):
        jwt.decode(invalid_token, SECRET_KEY, algorithms=[ALGORITHM])


def test_jwt_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "testuser"
