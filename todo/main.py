from fastapi import FastAPI
from .routers import todos_routers, users_routers, auth_routers
from .database import engine, Base
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_routers.router)
app.include_router(users_routers.router, prefix="/users", tags=["users"])
app.include_router(todos_routers.router, prefix="/todos", tags=["todos"])
