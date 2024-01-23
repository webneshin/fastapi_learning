from typing import Optional

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

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
    name: str = Path(min_length=2, max_length=100)
    age: int = Path(ge=18, le=100)
    height: int | None = None


@app.post("/04_query_path/user")
def query_path(person: Person2, page:int=Query(0, ge=0)):
    return person,page
