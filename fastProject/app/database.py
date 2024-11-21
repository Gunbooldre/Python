import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

SQLALCHEMY_DATABASE_URL = (f'postgresql://{settings.DATABASE_USERNAME}:'
                           f'{settings.DATABASE_PASSWORD}@'
                           f'{settings.DATABASE_HOSTNAME}:'
                           f'{settings.DATABASE_PORT}/'
                           f'{settings.DATABASE_NAME}')

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='123', port="5433",
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connected succesfully")
#         break
#     except Exception as e:
#         print("Connection to database failed")
#         print(f"Errors {e}")
