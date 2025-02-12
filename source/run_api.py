from fastapi import FastAPI

from .api.task_router import router as task_router
from .api.user_router import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(task_router)
