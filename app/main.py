from fastapi import FastAPI

from app.users.handlers import router as user_router


app: FastAPI = FastAPI()
app.include_router(user_router)
