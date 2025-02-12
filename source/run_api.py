from fastapi import FastAPI
from .api.user_router import router as user_router
from .api.task_router import router as task_router

app = FastAPI()

app.include_router(user_router)
app.include_router(task_router)
