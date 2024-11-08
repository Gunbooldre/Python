from typing import List

import psycopg2
from fastapi import Depends, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from app.schema import (Post, PostBase, PostCreate, PostUpdate,
                        UserCreateSchema, UsersOut)

from . import models, utils
from .database import engine, get_db

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


@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(data: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get('/posts/{id}', response_model=List[Post])
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(id == models.Post.id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    return post


@app.delete('/posts/{id}')
def delete_post(id: int,  db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(id == models.Post.id)

    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} does not exist ')

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",response_model=Post)
def update_post(id: int, data: PostUpdate, db: Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(id == models.Post.id)

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} does not exist ')

    updated_post.update(data.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UsersOut)
def create_user(data: UserCreateSchema, db: Session = Depends(get_db)):
    data.password = utils.hash(data.password)

    new_user = models.User(**data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
