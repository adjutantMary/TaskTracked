import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch
from ..run_api import app
from ..schemas.schemas import TaskBase
from ..models import crud

# Mock данные
mock_task = TaskBase(
    user_id=1, title="Sample Task", description="This is a sample task", due_date=None
)
mock_tasks = [mock_task]


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


# Тест для получения всех задач
@pytest.mark.asyncio
@patch("source.models.crud.TaskManager.find_all")
def test_get_all_tasks(mock_find_all, test_client):
    mock_find_all.return_value = mock_tasks

    response = test_client.get("/task-router/all-tasks")

    assert response.status_code == 200
    assert response.json() == [mock_task.dict()]


# Тест для создания задачи
@patch("source.models.crud.TaskManager.add")
def test_create_task(mock_add, test_client):
    mock_add.return_value = True

    response = test_client.post("/task-router/add-new-task/", json=mock_task.dict())

    assert response.status_code == 200
    assert response.json() == {
        "message": "Задача была успешно создана!",
        "task": mock_task.dict(),
    }


# Тест для обновления описания задачи
@patch("source.models.crud.TaskManager.update")
def test_update_task_description(mock_update, test_client):
    updated_task = TaskBase(
        user_id=1, title="Sample Task", description="Updated description", due_date=None
    )
    mock_update.return_value = True

    response = test_client.put(
        "/task-router/update-task-description/", json=updated_task.dict()
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Описание задачи обновлено",
        "task": updated_task.dict(),
    }


# Тест для удаления задачи
@patch("source.models.crud.TaskManager.delete")
def test_delete_task(mock_delete, test_client):
    task_title = "Sample Task"
    mock_delete.return_value = True

    response = test_client.delete(f"/task-router/delete-task/?task_title={task_title}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Задача {task_title} удалена"}
