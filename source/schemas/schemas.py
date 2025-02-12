from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# The `UserBase` class defines attributes for a user with optional username and email fields and a
# method to convert the object to a dictionary.
class UserBase(BaseModel):
    username: str | None = None
    email: str | None = None

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}


# The `TaskBase` class defines attributes for a task including user ID, title, description, and due
# date with optional values.
class TaskBase(BaseModel):
    user_id: int
    title: str
    description: str | None = None
    due_date: Optional[datetime] = None

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
        }
