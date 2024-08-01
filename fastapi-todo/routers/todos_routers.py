from typing import List
from fastapi import APIRouter, HTTPException
from ..crud import todo_crud
from ..schemas import todo_schemas
from ..auth import db_dependency, user_dependency

router = APIRouter()


@router.post("/", response_model=todo_schemas.Todo)
def create_todo(
    todo: todo_schemas.TodoCreate, db: db_dependency, current_user: user_dependency
):
    return todo_crud.create_user_todo(db=db, todo=todo, user_id=current_user.id)


@router.get("/", response_model=List[todo_schemas.Todo])
def read_todos(
    db: db_dependency,
    current_user: user_dependency,
    skip: int = 0,
    limit: int = 10,
):
    return todo_crud.get_todos(db, user=current_user, skip=skip, limit=limit)


@router.get("/getTodoById/{todo_id}", response_model=todo_schemas.Todo)
def read_todo(todo_id: int, db: db_dependency):
    db_todo = todo_crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.put("/updateTodoById/{todo_id}", response_model=todo_schemas.Todo)
def update_todo(todo_id: int, todo: todo_schemas.TodoUpdate, db: db_dependency):
    return todo_crud.update_todo(db=db, todo_id=todo_id, todo=todo)


@router.delete("/deleteTodoByID/{todo_id}", response_model=todo_schemas.Todo)
def delete_todo(todo_id: int, db: db_dependency):
    db_todo = todo_crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_crud.delete_todo(db=db, todo_id=todo_id)
    return db_todo
