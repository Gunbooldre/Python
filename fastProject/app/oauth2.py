from datetime import datetime, timedelta
from .database import engine, get_db
from app.models import User
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.schemas import TokenData

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "1e015e368796dd36461321b1a52c09097c17acea6839612a582b299d2c28668b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_current_user(token: str = Depends(oauth2_schema),db: Session =  Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not login",
                                          headers={"WWW-Authentificate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token.id).first()
    return user
    # return verify_access_token(token, credentials_exception)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = TokenData(id=str(id))

    except JWTError:
        raise credentials_exception

    return token_data
