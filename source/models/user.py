from datetime import date, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship

from .base import Base


class User(Base):
    """Модель пользователя"""

    __tablename__ = "user_task"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    username: Mapped[str] = mapped_column(
        "username", primary_key=True, nullable=False, unique=True
    )
    email: Mapped[str] = mapped_column(
        "email", primary_key=True, nullable=False, unique=True
    )
    # Связь "один ко многим" - один пользователь может иметь множество задач
    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="user", cascade="all, delete-orphan"
    )


class Task(Base):
    """Модель задачи"""

    __tablename__ = "task"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_task.id"))

    # Поле определяющее связь между двумя моделями
    user: Mapped[User] = relationship("User", back_populates="tasks")

    title: Mapped[str] = mapped_column("tittle", String(length=64), nullable=False)
    description: Mapped[str] = mapped_column("description", nullable=False, default="")
    due_date: Mapped[datetime] = mapped_column(
        "due_date", DateTime, default=datetime.now
    )

    def to_dict(self):
        return {
            "task_id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
        }
