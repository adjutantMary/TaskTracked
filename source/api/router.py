from fastapi import APIRouter, Depends
from ..schemas.schemas import *
from sqlalchemy import select 
from ..db import async_session_maker 
from ..models.user import *
from ..models.crud import *
from .request_body import *

router = APIRouter(prefix='/task-tracker', tags=['TaskTracked API service'])

# эндпоинт для получения всех пользователей - по тз не нужен
# @router.get("/all-users", summary="Получить всех пользователей")
# async def get_all_users(request_body: UserRequestBody = Depends()) -> list[UserBase]:
#     return await UserManager.find_all(**request_body.to_dict())



@router.get("/user-by-{id}", summary="Получить одного пользователя по id")
async def get_student_by_id(user_id: int) -> UserBase | None:
    rez = await UserManager.find_one_or_none_by_id(user_id)
    if rez is None:
        return {'message': f'Пользователь с ID {user_id} не найден!'}
    return rez

@router.get("/by_filter", summary="Получить одного студента по фильтру")
async def get_student_by_filter(request_body: UserRequestBody = Depends()) -> UserBase | dict:
    rez = await UserManager.find_one_or_none(**request_body.to_dict())
    if rez is None:
        return {'message': f'Студент с указанными вами параметрами не найден!'}
    return rez

@router.post("/add/")
async def register_user(user: UserBase) -> dict:
    user_data = user.model_dump(by_alias=True)
    check = await UserManager.add(**user_data)
    if check:
        return {"message": "Пользователь успешно добавлен!", "user": user}
    else:
        return {"message": "Ошибка при добавлении пользователя!"}
    