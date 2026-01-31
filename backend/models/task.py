from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

# Forward reference to User model
class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    priority: int = Field(default=1, ge=1, le=5)  # Priority levels 1-5, with 1 being highest
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user: "User" = Relationship(back_populates="tasks")

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[int] = Field(default=None, ge=1, le=5)

class TaskCreate(TaskBase):
    priority: int = Field(default=3, ge=1, le=5)  # Default to medium priority

class TaskRead(TaskBase):
    id: str
    user_id: str
    priority: int
    created_at: datetime
    updated_at: datetime