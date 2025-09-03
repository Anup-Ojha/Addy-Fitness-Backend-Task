from fastapi import FastAPI
from routes import users, auth
from app.database import engine, Base
app = FastAPI(title="Task Project - JWT Auth")
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router, prefix="/users", tags=["users"])
