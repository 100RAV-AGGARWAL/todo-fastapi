from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from auth import get_current_user
import crud, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[schemas.User, Depends(get_current_user)]

@router.post("/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: db_dependency,
                current_user: user_dependency):
    return crud.create_user_todo(db=db, todo=todo, user_id=current_user.id)


@router.get("/", response_model=List[schemas.Todo])
def read_todos(db: db_dependency, current_user: user_dependency, skip: int = 0, limit: int = 10, ):
    return crud.get_todos(db, user=current_user, skip=skip, limit=limit)


@router.get("/getTodoById/{todo_id}", response_model=schemas.Todo)
def read_todo(todo_id: int, db: db_dependency, current_user: user_dependency):
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.put("/updateTodoById/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: db_dependency,
                current_user: user_dependency):
    return crud.update_todo(db=db, todo_id=todo_id, todo=todo)


@router.delete("/deleteTodoByID/{todo_id}", response_model=schemas.Todo)
def delete_todo(todo_id: int, db: db_dependency, current_user: user_dependency):
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    crud.delete_todo(db=db, todo_id=todo_id)
    return db_todo
