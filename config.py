from fastapi import FastAPI, Request
from routers import users
from routers import app_first
import time

app = FastAPI()

app.include_router(app_first.router)
app.include_router(users.router, tags=['database'])


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time-calced'] = process_time.__str__()
    return response
