from fastapi import APIRouter, HTTPException
from typing import List
from ..auth import db_dependency
from ..crud import user_crud
from ..schemas import user_schemas

router = APIRouter()


@router.get("/", response_model=List[user_schemas.User])
def read_users(
    db: db_dependency,
    skip: int = 0,
    limit: int = 10,
):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=user_schemas.User)
def read_user(user_id: int, db: db_dependency):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=user_schemas.User)
def create_user(user: user_schemas.UserCreate, db: db_dependency):
    db_user = user_crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_crud.create_user(db=db, user=user)
