from fastapi import FastAPI

from app.users.handlers import router as user_router
from app.auth.handlers import router as auth_router


app: FastAPI = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
