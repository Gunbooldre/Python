from app.schemas.schemas import *
from jose import jwt
import pytest
from app.config import settings


def test_root(client):
    res = client.get("/")
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "Dias3@gmail.com", "password": "123"})
    new_user = UsersOut(**res.json())
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login/", data={"username": test_user['email'], "password": test_user["password"]})
    login_res = Token(**res.json())
    payload =jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type == "Bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("123@gmail.com", "123", 403),
    ("124@gmail.com", "124", 403),
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    assert res.json().get('detail') == 'Email is not found'
