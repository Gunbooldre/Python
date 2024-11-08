from typing import List

from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from sqlalchemy.orm import Session

from app.schemas import Post, PostCreate, PostUpdate

from .. import models
from ..database import engine, get_db

router = APIRouter(prefix="/posts", tags=["Post"])


@router.get("/test")
def root(db: Session = Depends(get_db)):
    return {"message": "Hello World"}


@router.get("/")
async def get_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(data: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=List[Post])
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(id == models.Post.id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    return post


@router.delete('/{id}')
def delete_post(id: int,  db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(id == models.Post.id)

    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} does not exist ')

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Post)
def update_post(id: int, data: PostUpdate, db: Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(id == models.Post.id)

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} does not exist ')

    updated_post.update(data.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()