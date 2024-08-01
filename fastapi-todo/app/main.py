from fastapi import FastAPI
from routers import todos, users, auth
from database import engine
import models
from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(todos.router, prefix="/todos", tags=["todos"])
