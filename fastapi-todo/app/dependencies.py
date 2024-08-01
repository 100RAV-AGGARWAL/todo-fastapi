from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import database
import auth


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
token_dependency = Annotated[str, Depends(auth.oauth2_bearer)]


async def get_current_user(token: token_dependency, db: db_dependency):
    return await auth.get_current_user(token, db)
