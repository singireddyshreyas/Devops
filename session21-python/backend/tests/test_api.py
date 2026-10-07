import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from sqlalchemy.engine import URL
from fastapi.testclient import TestClient
from app.main import app
from app.config import Settings

client = TestClient(app)

def test_health():
    assert client.get("/health").json() == {"status": "UP"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "TaskBoard API"

def test_create_task_validation():
    response = client.post("/api/tasks", json={"title": "Deploy application", "priority": "HIGH", "assignee": "Student"})
    assert response.status_code == 201
    assert response.json()["title"] == "Deploy application"

def test_database_settings_escape_credentials():
    settings = Settings(
        database_url=None,
        db_host="postgres",
        db_port=5432,
        db_name="taskboard",
        db_user="student",
        db_password="test@local/path",
    )

    url = settings.sqlalchemy_url

    assert isinstance(url, URL)
    assert url.username == "student"
    assert url.password == "test@local/path"
    assert url.host == "postgres"
