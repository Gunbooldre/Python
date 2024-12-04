from app.schemas import *
from .database import client, db


def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Hello World my friend"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "Dias3@gmail.com", "password": "123"})
    new_user = UsersOut(**res.json())
    print(new_user.email)
    assert res.status_code == 201
