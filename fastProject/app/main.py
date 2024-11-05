import psycopg2
from fastapi import Depends, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from schema import Post

from . import models
from .database import SessionLocal, engine, get_db

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
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(data: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(id == models.Post.id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    return {"data": post}


@app.delete('/posts/{id}')
def delete_post(id: int,  db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(id == models.Post.id)

    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} does not exist ')

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, data: Post, db: Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(id == models.Post.id)

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} does not exist ')

    updated_post.update(data.dict(), synchronize_session=False)
    db.commit()
    return {"data": updated_post.first()}
