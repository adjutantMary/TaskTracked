from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship
from .base import Base



class User(Base):
    """Модель пользователя"""
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    username: Mapped[str] = mapped_column(
        "username", primary_key=True, nullable=False, unique=True
    )
    email: Mapped[str] =  mapped_column(
        "email", primary_key=True, nullable=False, unique=True
    )
    
