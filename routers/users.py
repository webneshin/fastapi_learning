from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from dependencies import get_db
from schemas import users as schemas
from models import users as models


router = APIRouter()

# database #############################################################################################################
# models.Base.metadata.create_all(bind=engine)


@router.post("/07_database/users", response_model=schemas.User)
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


@router.get("/07_database/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user
