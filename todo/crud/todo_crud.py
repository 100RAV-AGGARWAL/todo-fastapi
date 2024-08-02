from sqlalchemy.orm import Session
from ..models import todo_models
from passlib.context import CryptContext
from ..schemas import todo_schemas, user_schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_todos(db: Session, user: user_schemas.User, skip: int = 0, limit: int = 10):
    return (
        db.query(todo_models.Todo)
        .filter(todo_models.Todo.owner_id == user.id)
        .offset(skip)
        .limit(limit)
    )


def create_user_todo(db: Session, todo: todo_schemas.TodoCreate, user_id: int):
    db_todo = todo_models.Todo(**todo.model_dump(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todo(db: Session, todo_id: int):
    return db.query(todo_models.Todo).filter(todo_models.Todo.id == todo_id).first()


def delete_todo(db: Session, todo_id: int):
    db.query(todo_models.Todo).filter(todo_models.Todo.id == todo_id).delete()
    db.commit()


def update_todo(db: Session, todo_id: int, todo: todo_schemas.TodoUpdate):
    db_todo = db.query(todo_models.Todo).filter(todo_models.Todo.id == todo_id).first()
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo
