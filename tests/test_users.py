from app import schemas
from jose import jwt
from app.config import settings
from app.oauth2 import ALGORITHM
import pytest

def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == "Welcome to my API"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users", json={"email": "test@test.com", "username": "test", "password": "test"})
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "test@test.com"
    assert res.status_code == 201
    
def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['username'], "password": test_user['password']})
    token_response = schemas.Token(**res.json())
    payload = jwt.decode(token=token_response.access_token, key=settings.secret_key, algorithms=[ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert token_response.token_type == "bearer"
    assert res.status_code == 200
    
@pytest.mark.parametrize("username, password, status_code", [
    ("test", "wrongPassword", 403),
    ("testWrongUsername", "test", 403),
    ("testWrongUsername", "wrongPassword", 403),
    (None, "test", 422),
    ("test", None, 422)
])
def test_incorrect_login(test_user, client, username, password, status_code):
    res = client.post("/login/", data={"username": username, "password": password})
    assert res.status_code == status_code
