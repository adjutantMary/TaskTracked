from fastapi import APIRouter, Depends
from ..schemas.schemas import *
from sqlalchemy import select 
from ..db import async_session_maker 
from ..models.user import *
from ..models.crud import *
from .request_body import *

router = APIRouter(prefix='/task-tracker', tags=['TaskTracked API service'])


@router.get("/all-users", summary="Получить всех пользователей")
async def get_all_users(request_body: UserRequestBody = Depends()) -> list[UserBase]:
    return await UserManager.find_all(**request_body.to_dict())

@router.get("/user-by-{id}", summary="Получить одного пользователя по id")
async def get_student_by_id(user_id: int) -> UserBase | None:
    rez = await UserManager.find_one_or_none_by_id(user_id)
    if rez is None:
        return {'message': f'Пользователь с ID {user_id} не найден!'}
    return rez

@router.post("/add/")
async def register_user(user: UserBase) -> dict:
    user_data = user.model_dump(by_alias=True)
    print(user_data)
    check = await UserManager.add(**user_data)
    if check:
        return {"message": "Пользователь успешно добавлен!", "user": user}
    else:
        return {"message": "Ошибка при добавлении пользователя!"}
    