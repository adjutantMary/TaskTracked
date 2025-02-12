from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError

from ..db import async_session_maker
from .user import Task, User


# The `BaseManager` class provides asynchronous methods for common database operations like finding,
# adding, updating, and deleting records using SQLAlchemy in Python.
class BaseManager:
    # The line `model = None` in the `BaseManager` class is initializing a class attribute `model`
    # with a default value of `None`. 
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                except Exception as e:
                    await session.rollback()
                    return None
                return new_instance

    @classmethod
    async def update(cls, filter_by, **values):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    update(cls.model)
                    # обновляем только те записи, которые соответствуют фильтрам
                    .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                    .values(**values)
                    .execution_options(synchronize_session="fetch")
                )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount  # возвращаем количество обновленных строк

    @classmethod
    async def delete(cls, delete_all: bool = False, **filter_by):
        if not delete_all and not filter_by:
            raise ValueError("Необходимо указать хотя бы один параметр для удаления.")

        async with async_session_maker() as session:
            async with session.begin():
                query = delete(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount


# The code defines two manager classes, UserManager and TaskManager, each associated with a specific
# model (User and Task, respectively).
class UserManager(BaseManager):
    model = User


class TaskManager(BaseManager):
    model = Task
