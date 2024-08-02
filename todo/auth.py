from datetime import datetime, timedelta
from typing import Annotated, Optional
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from .crud import user_crud
from .config import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from .database import SessionLocal
from .schemas import user_schemas


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
token_dependency = Annotated[str, Depends(oauth2_bearer)]


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: token_dependency, db: db_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = user_crud.get_user_by_username(db, username=username)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


user_dependency = Annotated[user_schemas.User, Depends(get_current_user)]
