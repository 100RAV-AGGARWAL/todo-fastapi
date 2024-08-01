from pydantic import BaseModel, EmailStr
from typing import List
from .todo_schemas import Todo


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    todos: List[Todo] = []

    class Config:
        orm_mode = True
