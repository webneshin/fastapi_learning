from fastapi import FastAPI, Path, Query, status, HTTPException, Request, Depends
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal
import schemas

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


# database #############################################################################################################
# models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/07_database/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    user = models.User(
        username=user.username,
        fullname=user.fullname,
        password=user.password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/07_database/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

# alembic ##############################################################################################################

# make migrations with:
# alembic revision --autogenerate -m "create user model"

# migration with:
# alembic upgrade head
# or
# alembic upgrade a48a95c818e3

# downgrade
# alembic downgrade a48a95c818e3
