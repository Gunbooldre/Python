
import psycopg2
from fastapi import Depends, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor

from . import models, utils
from .database import engine, get_db
from .routers import post, users

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='123', port="5433",
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected succesfully")
        break
    except Exception as e:
        print("Connection to database failed")
        print(f"Errors {e}")


app.include_router(post.router)
app.include_router(users.router)
