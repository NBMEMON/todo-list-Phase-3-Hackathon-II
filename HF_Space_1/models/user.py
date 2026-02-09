from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
import bcrypt


class UserBase(SQLModel):
    username: str = Field(min_length=3, max_length=50, unique=True)
    email: str = Field(min_length=5, max_length=100, unique=True)
    name: Optional[str] = Field(default=None, max_length=100)


class User(UserBase, table=True):
    __tablename__ = "users"  # Use a non-reserved word as table name
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    password_hash: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)
    password_hash: Optional[str] = Field(default=None, min_length=1)

    def hash_password(self):
        """Hash the password before storing"""
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        self.password_hash = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # Clear plain text passwords after hashing
        delattr(self, 'password')
        delattr(self, 'confirm_password')


class UserUpdate(SQLModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    name: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = Field(default=None, min_length=5, max_length=100)


class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime