from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.schemas import Post, PostCreate, PostOut, PostUpdate, PaginationParams

from .. import models, oauth2
from ..database import get_db
from ..utils import pagination_dep

router = APIRouter(prefix="/posts", tags=["Post"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[PostOut])
async def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    pagination: PaginationParams = Depends(pagination_dep),
    search: Optional[str] = "",
):
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(pagination.limit)
        .offset(pagination.skip)
        .all()
    )
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    user_id: models.User = Depends(oauth2.get_current_user),
):
    new_post = models.Post(owner_id=user_id.id, **data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(id == models.Post.id)
        .first()
    )

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )

    return post


@router.delete("/{id}")
def delete_post(
    _id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    deleted_post = db.query(models.Post).filter(_id == models.Post.id)
    post = deleted_post.first()

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform requested action",
        )

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Post)
def update_post(
    _id: int,
    data: PostUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    updated_post = db.query(models.Post).filter(_id == models.Post.id)
    post = updated_post.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with ID {_id} does not exist ",
        )

    updated_post.update(data.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()
