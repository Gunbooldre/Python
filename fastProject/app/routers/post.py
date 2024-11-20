from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.schemas import Post, PostCreate, PostUpdate

from .. import models, oauth2
from ..database import engine, get_db

router = APIRouter(prefix="/posts", tags=["Post"])


@router.get("/")
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).all()
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(data: PostCreate, db: Session = Depends(get_db), user_id: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=user_id.id,  **data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=List[Post])
def get_post(id: int, db: Session = Depends(get_db),  current_user:  models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(id == models.Post.id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")


    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized to perform requested action')

    return post


@router.delete('/{id}')
def delete_post(id: int,  db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(id == models.Post.id)
    post = deleted_post.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} does not exist ')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized to perform requested action')

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Post)
def update_post(id: int, data: PostUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    updated_post = db.query(models.Post).filter(id == models.Post.id)

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} does not exist ')

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized to perform requested action')

    updated_post.update(data.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()