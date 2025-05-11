from fastapi.testclient import TestClient
import pytest
from app.main_sqlalchemy import app
from app import models, schemas
from app.config import settings
from app.database import get_db
from alembic import command
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    # If we don't use alembic, we should drop and create tables manually
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    # after yield statement we can run some more code
    # If we use alembic
    # command.upgrade("head")
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # command.downgrade("base")

@pytest.fixture
def test_user2(client: TestClient):  # noqa: F811
    user_data = {
        "email": "54yWZ1v@example.com",
        "password": "password123",
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user(client: TestClient):  # noqa: F811
    user_data = {
        "email": "54yWZv@example.com",
        "password": "password123",
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user.get("id")})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}",
    }

    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user.get("id"),
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user.get("id"),
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user.get("id"),
        },
        {
            "title": "fourth title",
            "content": "fourth content",
            "owner_id": test_user2.get("id"),
        }
    ]

    session.add_all([models.Post(**post) for post in posts_data])
    session.commit()
    posts = session.query(models.Post).all()
    return posts