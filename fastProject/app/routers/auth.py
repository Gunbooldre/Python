from fastapi import APIRouter, Depends, status, HTTPException, Response
from ..database import engine, get_db
from .. import models, utils

from sqlalchemy.orm import Session
from app.schemas import UserLogin


router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    print(user.emailv )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Email is not found")

    if not utils.verify(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Password is wrong")
    token = {}
    return token

