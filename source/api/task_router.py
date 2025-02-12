from fastapi import APIRouter, Depends, HTTPException
from ..schemas.schemas import *
from sqlalchemy import select
from ..db import async_session_maker
from ..models.user import *
from ..models.crud import *
from .request_body import *


router = APIRouter(prefix="/task-router", tags=['Task"s endpoints'])


@router.get("/all-tasks", summary="Получить либо все задачи, либо по фильтру")
async def get_all_tasks(request_body: TaskRequestBody = Depends()) -> list[TaskBase]:
    return await TaskManager.find_all(**request_body.to_dict())


@router.get("/task-by-user", summary="Получить задачи пользователя по его id")
async def get_student_by_id(user_id: str) -> TaskBase | None:
    rez = await TaskManager.find_one_or_none_by_id(user_id)
    if rez is None:
        raise HTTPException(
            status_code=500,
            detail={"message": f"Задачи пользователя с ID {user_id} не найдены!"},
        )
    return rez


@router.post("/add-new-task/", summary="Создание новой задачи")
async def register_user(task: TaskBase) -> dict:
    task_data = task.model_dump(by_alias=True)
    check = await TaskManager.add(**task_data)
    if check:
        return {"message": "Задача была успешно создана!", "task": task}
    else:
        return {"message": "Ошибка при создании задачи!"}


@router.put("/update-task-description/", summary="Обновление описания задачи")
async def update_task_description(task: TaskBase) -> dict:
    check = await TaskManager.update(
        filter_by={"title": task.title}, description=task.description
    )
    if check:
        return {"message": "Описание задачи обновлено", "task": task}
    else:
        return {"message": "Ошибка при обновлении задачи"}


@router.delete("/delete-task/", summary="Удаление задачи")
async def delete_task(task_title: str) -> dict:
    check = await TaskManager.delete(title=task_title)
    if check:
        return {"message": f"Задача {task_title} удалена"}
    else:
        return {"message": "Ошибка при удалении"}
