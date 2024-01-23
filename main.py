from typing import Optional

from fastapi import FastAPI, Path, Query, status, HTTPException, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# app ##################################################################################################################
@app.get("/01_app/get_method")
async def get_method():
    return "this is 'get' method"


@app.post("/01_app/post_method")
async def post_method():
    return "this is 'post' method"


@app.put("/01_app/put_method")
async def put_method():
    return "this is 'put' method"


# parameters ###########################################################################################################
@app.get("/02_parameters/path_parameters/{name}/{age}")
async def path_parameter(name: str, age: int):
    return {"message": f"{name} is {age} years old.."}


@app.get("/02_parameters/query_parameters/{name}")
async def path_parameter(name: str, age: int = 38):
    return {"message": f"{name} is {age} years old."}


# request body #########################################################################################################
class Person(BaseModel):
    name: str
    age: int
    height: int | None = None


@app.post("/03_request_body/user")
def request_body(person: Person):
    return person


# query path ###########################################################################################################
class Person2(BaseModel):
    name: str = Path(min_length=2, max_length=100, title="Fullname", description="firstname and lastname of user")
    age: int = Path(ge=18, le=100)
    height: int | None = None


@app.post("/04_query_path/user")
def query_path(person: Person2, page: int = Query(0, ge=0)):
    return person, page


# response model #######################################################################################################

class UserCreate(BaseModel):
    username: str
    fullname: str
    password: str


class UserMe(BaseModel):
    username: str
    fullname: str


@app.post("/05_response_model/user", response_model=UserMe, status_code=status.HTTP_201_CREATED)
def response_model(user: UserCreate):
    if user.username == "admin":
        # raise Exception("username can not be 'admin'")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username can not be 'admin'")
    return user


# template #############################################################################################################
templates = Jinja2Templates(directory="templates")


@app.get("/06_template/home", response_class=HTMLResponse)
def template_sample(request: Request):
    user_username = "webneshin"
    return templates.TemplateResponse('home.html', {"request": request, "user_username": user_username})
