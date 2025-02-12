import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch
from ..run_api import app
from ..schemas.schemas import UserBase
from ..models import crud
from ..api.request_body import UserRequestBody


mock_user = UserBase(id=1, username="testuser", email="test@example.com")


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


# Тест для получения пользователя по ID
@patch("source.models.crud.UserManager.find_one_or_none_by_id")
def test_get_user_by_id(mock_find_one_or_none_by_id, test_client):
    user_id = 1
    mock_find_one_or_none_by_id.return_value = mock_user

    response = test_client.get(f"/user-router/user-by-id?user_id={user_id}")

    assert response.status_code == 200
    assert response.json() == mock_user.dict()


# Тест для получения пользователя по фильтру
@patch("source.models.crud.UserManager.find_one_or_none")
def test_get_user_by_filter(mock_find_one_or_none, test_client):
    request_body = UserRequestBody(username="testuser", email="test@example.com")
    mock_find_one_or_none.return_value = mock_user

    response = test_client.get("/user-router/by-filter", params=request_body.to_dict())

    assert response.status_code == 200
    assert response.json() == mock_user.dict()


# Тест для регистрации нового пользователя
@patch("source.models.crud.UserManager.add")
def test_register_user(mock_add, test_client):
    mock_add.return_value = True

    response = test_client.post("/user-router/add-new-user/", json=mock_user.dict())

    assert response.status_code == 200
    assert response.json() == {
        "message": "Пользователь успешно добавлен!",
        "user": mock_user.dict(),
    }


# Тест для случая, когда пользователь не найден по фильтру
@patch("source.models.crud.UserManager.find_one_or_none")
def test_get_user_by_filter_not_found(mock_find_one_or_none, test_client):
    request_body = UserRequestBody(username="unknownuser", email="unknown@example.com")
    mock_find_one_or_none.return_value = None

    response = test_client.get("/user-router/by-filter", params=request_body.to_dict())

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Пользователь с указанными вами параметрами не найден!"
    }


# Тест для случая, когда пользователь не найден по ID
@patch("source.models.crud.UserManager.find_one_or_none_by_id")
def test_get_user_by_id_not_found(mock_find_one_or_none_by_id, test_client):
    user_id = 1
    mock_find_one_or_none_by_id.return_value = None
    response = test_client.get(f"/user-router/user-by-id?user_id={user_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Пользователь с ID {user_id} не найден!"}
