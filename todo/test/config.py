from datetime import timedelta

import bcrypt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from todo.main import app
from todo.database import Base
from todo.auth import get_current_user, create_access_token, get_db
from todo.models.user_models import User
from todo.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

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
    db = TestingSessionLocal()
    user = db.query(User).filter(User.username == "testuser").first()
    db.close()
    return user


app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture
def db():
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture
def test_user(db):
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(text(f"TRUNCATE TABLE {table.name} CASCADE"))
    db.commit()

    hashed_password = bcrypt.hashpw("testpassword".encode("utf-8"), bcrypt.gensalt())
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password=hashed_password.decode("utf-8"),
        is_active=True,
        is_admin=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def token(test_user):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        data={"sub": test_user.username}, expires_delta=access_token_expires
    )


@pytest.fixture
def authorized_client(token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}",
    }
    return client


# @pytest.hookimpl(tryfirst=True)
# def pytest_sessionfinish(session, exitstatus):
#     for table in reversed(Base.metadata.sorted_tables):
#         engine.connect().execute(text(f"TRUNCATE TABLE {table.name} CASCADE"))


# @pytest.fixture(autouse=True)
# def clear_db():
#     yield
#     for table in reversed(Base.metadata.sorted_tables):
#         engine.connect().execute(text(f"TRUNCATE TABLE {table.name} CASCADE"))
