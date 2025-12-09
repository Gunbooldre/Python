from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.schemas import Token

from .. import models, utils
from ..utils import oauth2
from app.db.database import get_db

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Email is not found"
        )

    if not utils.verify(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Password is wrong"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "Bearer"}
