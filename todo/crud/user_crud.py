from sqlalchemy.orm import Session
from ..models import user_models
from passlib.context import CryptContext
from ..schemas import user_schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_username(db: Session, username: str):
    return (
        db.query(user_models.User).filter(user_models.User.username == username).first()
    )


def get_user(db: Session, user_id: int):
    return db.query(user_models.User).filter(user_models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(user_models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user_schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = user_models.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
