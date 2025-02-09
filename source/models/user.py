from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship
from .base import Base
from datetime import datetime, date



class User(Base):
    """Модель пользователя"""

    __tablename__ = "user"

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
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user", cascade="all, delete-orphan")


class Task(Base):
    """Модель задачи"""

    __tablename__ = "task"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    #Поле определяющее связь между двумя моделями
    user: Mapped[User] = relationship("User", back_populates="tasks")

    tittle: Mapped[str] = mapped_column("tittle", String(length=64), nullable=False)
    description: Mapped[str] = mapped_column("description", nullable=False, default="")
    due_date: Mapped[datetime] = mapped_column(
        "due_date", DateTime, default=datetime.now
    )

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d["id"] = str(self.id)
        d["due_date"] = self.due_date.replace(microsecond=0).isoformat()
        return d

