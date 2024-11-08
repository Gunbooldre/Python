from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from sqlalchemy.orm import Session

from app.schemas import (Post, PostBase, PostCreate, PostUpdate,
                         UserCreateSchema, UsersOut)

from .. import models, utils
from ..database import engine, get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UsersOut)
def create_user(data: UserCreateSchema, db: Session = Depends(get_db)):
    data.password = utils.hash(data.password)

    new_user = models.User(**data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=UsersOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with this {id} is not found")
    return user
