from fastapi.testclient import TestClient
import pytest
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import get_db, Base

from app.utils.oauth2 import create_access_token
from app.config import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.DATABASE_USERNAME}:"
    f"{settings.DATABASE_PASSWORD}@"
    f"{settings.DATABASE_HOSTNAME}:"
    f"{settings.DATABASE_PORT}/"
    f"{settings.DATABASE_NAME}_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# docker exec -it fastproject-api-1 alembic upgrade head


@pytest.fixture()
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client):
    data = {"email": "Dias3@gmail.com", "password": "123"}
    res = client.post("/users/", json=data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client
