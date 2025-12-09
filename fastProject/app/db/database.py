from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.DATABASE_USERNAME}:"
    f"{settings.DATABASE_PASSWORD}@"
    f"{settings.DATABASE_HOSTNAME}:"
    f"{settings.DATABASE_PORT}/"
    f"{settings.DATABASE_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# docker exec -it fastproject-api-1 alembic upgrade head


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
