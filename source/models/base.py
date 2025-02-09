from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


convention = {
    "ix": "ix_%(column_0_label)s",  # перфикс индекса
    "uq": "uq_%(table_name)s_%(column_0_name)s",  # префикс ограничений
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # префикс ограничений проверок
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # префикс foreign_key
    "pk": "pk_%(table_name)s",  # префикс primary_key
}


class Base(DeclarativeBase):
    """Родительский базовый класс моделей"""

    __abstract__ = True

    # передаем конвенцию чтобы все модели могли автоматически их использовать
    metadata = MetaData(naming_convention=convention)

    def __repr__(self) -> str:
        """Создание строкового представления экземпляра класса"""
        columns = ", ".join(
            [
                f"{k}={repr(v)}"
                for k, v in self.__dict__.items()
                if not k.startswith("_")
            ]
        )
        return f"<{self.__class__.__name__}({columns})>"
