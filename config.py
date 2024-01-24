from fastapi import FastAPI
from routers import users
from routers import app_first

app = FastAPI()

app.include_router(app_first.router)
app.include_router(users.router,tags=['database'])
