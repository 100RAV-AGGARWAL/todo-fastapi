import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from todo.main import app
from todo.database import Base
from todo.auth import get_current_user, create_access_token, get_db
from todo.models.user_models import User
from todo.config import SECRET_KEY, ALGORITHM

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost/test_tododb"
SECRET_KEY = SECRET_KEY
ALGORITHM = ALGORITHM

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def override_get_current_user():
    user_dict = {
        "id": 1,
        "username": "testuser",
        "email": "testuser@example.com",
        "is_active": True,
        "is_admin": True,
        "todos": [],
    }
    return User(**user_dict)


app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture(scope="module")
def db():
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture(scope="module")
def test_user(db):
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="$2b$12$KIXtCrf/4ogHBBi",
        is_active=True,
        is_admin=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="module")
def token(test_user):
    return create_access_token(data={"sub": test_user.username})


@pytest.fixture(scope="module")
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}",
    }
    return client
