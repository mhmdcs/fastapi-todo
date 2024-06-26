from app import schemas
import pytest

def test_get_all_tasks(authorized_client, test_tasks):
    res = authorized_client.get("/tasks")
    assert res.status_code == 200
    
def test_unauthorized_user_get_all_tasks(client, test_tasks):
    res = client.get("/tasks")
    assert res.status_code == 401
    
def test_unauthorized_user_get_one_tasks(client, test_tasks):
    res = client.get(f"/tasks/{test_tasks[0].id}")
    assert res.status_code == 401
    
def test_get_one_nonexistent_task(authorized_client, test_tasks):
    res = authorized_client.get(f"/task/543")
    assert res.status_code == 404
    
def test_get_one_task(authorized_client, test_tasks):
    res = authorized_client.get(f"/tasks/{test_tasks[0].id}")
    task = schemas.TaskResponse(**res.json())
    assert res.status_code == 200
    assert task.id == test_tasks[0].id
    assert task.content == test_tasks[0].content
    assert task.title == test_tasks[0].title
    
@pytest.mark.parametrize("title, content, done", [
    ("tests!", "writing some tests!", True),
    ("testing yet another title", "another content test", False),
    ("another title test", "another content tests", False),
])
def test_create_task(authorized_client, test_user, title, content, done):
    res = authorized_client.post("/tasks", json={"title": title, "content": content, "done": done})
    assert res.status_code == 201
    created_task = schemas.TaskResponse(**res.json())
    assert created_task.title == title
    assert created_task.content == content
    assert created_task.done == done
    assert created_task.owner_id == test_user['id']
    
    
def test_create_task_with_default_done(authorized_client):
    res = authorized_client.post("/tasks", json={"title": "some placeholder title", "content": "some placeholder content"})
    created_task = schemas.TaskResponse(**res.json())
    assert created_task.done == False
    assert res.status_code == 201
    
def test_unauthorized_user_create_task(client):
    res = client.post("/tasks", json={"title": "some placeholder title", "content": "some placeholder content"})
    assert res.status_code == 401
    
def test_delete_task(authorized_client, test_tasks):
    res = authorized_client.delete(f"/tasks/{test_tasks[0].id}")
    assert res.status_code == 204
    
def test_delete_nonexistent_task(authorized_client, test_tasks):
    res = authorized_client.delete("/tasks/73452")
    assert res.status_code == 404
    
def test_delete_other_user_task(authorized_client, test_tasks):
    res = authorized_client.delete(f"/tasks/{test_tasks[3].id}")
    assert res.status_code == 403
    
def test_unauthorized_user_delete_task(client, test_tasks):
    res = client.delete(f"/tasks/{test_tasks[0].id}")
    assert res.status_code == 401
    
def test_update_task(authorized_client, test_user, test_tasks):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_tasks[0].id
    }
    res = authorized_client.put(f"/tasks/{test_tasks[0].id}", json=data)
    updated_task = schemas.TaskResponse(**res.json())
    assert res.status_code == 200
    assert updated_task.title == data['title']
    assert updated_task.content == data['content']


def test_update_other_user_task(authorized_client, test_user, test_user2, test_tasks):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_tasks[3].id
    }
    res = authorized_client.put(f"/tasks/{test_tasks[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_task(client, test_user, test_tasks):
    res = client.put(f"/tasks/{test_tasks[0].id}")
    assert res.status_code == 401


def test_update_task_non_exist(authorized_client, test_user, test_tasks):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_tasks[3].id
    }
    res = authorized_client.put(f"/tasks/8000000", json=data)
    assert res.status_code == 404