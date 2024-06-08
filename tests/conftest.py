from fastapi.testclient import TestClient
from app.main import app
from app.oauth2 import create_access_token
from app import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from alembic import command
from starlette.datastructures import MutableHeaders
import pytest

DATABASE_CONNECTION_STRING = "postgresql+psycopg2://postgres:password@localhost:5432/fastapi-todo-test"

engine = create_engine(DATABASE_CONNECTION_STRING)

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)

@pytest.fixture
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
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user2(client):
    user_data = {"email": "test2@test.com", "username": "test2", "password": "test"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {"email": "test@test.com", "username": "test", "password": "test"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_tasks(test_user, test_user2, session):
    tasksDict = [
        {"title": "first title",
         "content": "first content",
         "owner_id": test_user['id']},
        {"title": "second title",
         "content": "second content",
         "owner_id": test_user['id']},
        {"title": "third title",
         "content": "third content",
         "owner_id": test_user['id']},
        {"title": "fourth title",
         "content": "fourth content",
         "owner_id": test_user2['id']}
    ]
    
    def create_task_model(task):
        return models.Task(**task)
        
    tasksModel = map(create_task_model, tasksDict)
    taskList = list(tasksModel)
    session.add_all(taskList)
    session.commit()
    tasks = session.query(models.Task).all()
    return tasks

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client