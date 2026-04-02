import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_list_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Read the code"})
    assert response.status_code == 201
    body = response.get_json()
    assert body["title"] == "Read the code"
    assert body["done"] is False


def test_create_task_requires_title(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 400
