from fastapi.testclient import TestClient

from app import models
from app.main import app
from app.schemas import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base

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
Base.metadata.create_all(bind=engine)
# docker exec -it fastproject-api-1 alembic upgrade head


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_root():
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Hello World my friend"
    assert res.status_code == 200


def test_create_user():
    res = client.post("/users/", json={"email": "Dias3@gmail.com", "password": "123"})
    new_user = UsersOut(**res.json())
    print(new_user.email)
    assert res.status_code == 201
