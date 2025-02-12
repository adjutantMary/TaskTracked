from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from ..db import async_session_maker
from ..models.crud import *
from ..models.user import *
from ..schemas.schemas import *
from .request_body import *

router = APIRouter(prefix="/user-router", tags=['User"s endpoints'])


@router.get("/user-by-id", summary="Получить одного пользователя по id")
async def get_user_by_id(user_id: int) -> UserBase:
    rez = await UserManager.find_one_or_none_by_id(user_id)
    if rez is None:
        raise HTTPException(
            status_code=404, detail=f"Пользователь с ID {user_id} не найден!"
        )
    return rez


@router.get("/by-filter", summary="Получить одного пользователя по фильтру")
async def get_user_by_filter(
    request_body: UserRequestBody = Depends(),
) -> UserBase:
    rez = await UserManager.find_one_or_none(**request_body.to_dict())
    if rez is None:
        raise HTTPException(
            status_code=404,
            detail="Пользователь с указанными вами параметрами не найден!",
        )
    return rez


@router.post("/add-new-user/", summary="Регистрация нового пользователя")
async def register_user(user: UserBase) -> dict:
    user_data = user.model_dump(by_alias=True)
    check = await UserManager.add(**user_data)
    if check:
        return {"message": "Пользователь успешно добавлен!", "user": user}
    else:
        return {"message": "Ошибка при добавлении пользователя!"}
