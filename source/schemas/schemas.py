from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import List, Optional



class UserBase(BaseModel):
    id: int 
    username: str | None = None
    email: str | None = None
    # tasks: list["TaskBase"] | None = None
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }
    
    
class TaskBase(BaseModel):
    id: int 
    user_id: int
    title: str
    description: str | None = None
    due_date: datetime = None



