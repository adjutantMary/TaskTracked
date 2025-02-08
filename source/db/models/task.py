from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship
from .base import Base

from datetime import datetime, date



class Task(Base):
    """Модель задачи"""
    __tablename__ = "task"
    
    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    tittle: Mapped[str] = mapped_column(
        "tittle", String(length=64), nullable=False
    )
    description: Mapped[str] =  mapped_column(
        "description", nullable=False, default=""
    )
    due_date: Mapped[datetime] = mapped_column(
        "due_date", DateTime, default=datetime.now
    )
    
    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d["id"] = str(self.id)
        d["due_date"] = self.due_date.replace(
            microsecond=0
        ).isoformat()
        return d