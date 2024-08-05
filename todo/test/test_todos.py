from .config import *


@pytest.fixture
def create_todo_payload():
    return {
        "title": "Test ToDo",
        "description": "Test Description",
        "completed": False,
    }


@pytest.fixture
def invalid_todo_payload():
    return {}  # Invalid


def test_create_invalid_todo(authorized_client, invalid_todo_payload):
    response = authorized_client.post("/todos/", json=invalid_todo_payload)
    assert response.status_code == 422  # Unprocessable Entity


def test_create_todo(authorized_client, create_todo_payload):
    response = authorized_client.post("/todos/", json=create_todo_payload)
    assert response.status_code == 200
    assert response.json()["title"] == create_todo_payload["title"]


def test_read_all_todos(authorized_client, create_todo_payload):
    authorized_client.post("/todos/", json=create_todo_payload)
    response = authorized_client.get("/todos/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_read_todo_by_id(authorized_client, create_todo_payload):
    response = authorized_client.post("/todos/", json=create_todo_payload)
    todo_id = response.json()["id"]
    response = authorized_client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == create_todo_payload["title"]


def test_read_todo_not_found(authorized_client):
    response = authorized_client.get("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_update_todo(authorized_client, create_todo_payload):
    response = authorized_client.post("/todos/", json=create_todo_payload)
    todo_id = response.json()["id"]
    update_payload = {"title": "Updated ToDo", "description": "Updated Description"}
    response = authorized_client.put(f"/todos/{todo_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["title"] == update_payload["title"]


def test_update_todo_not_found(authorized_client):
    update_payload = {"title": "Updated ToDo", "description": "Updated Description"}
    response = authorized_client.put("/todos/999", json=update_payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_delete_todo(authorized_client, create_todo_payload):
    response = authorized_client.post("/todos/", json=create_todo_payload)
    todo_id = response.json()["id"]
    response = authorized_client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200


def test_delete_todo_not_found(authorized_client):
    response = authorized_client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
