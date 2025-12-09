from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.votes import Vote

from app.models import models
from ..utils import oauth2
from app.db.database import get_db

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    data: Vote,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == data.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{data.post_id}"
        )
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == data.post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if data.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The {current_user.id} has already voted on post {data.post_id}",
            )
        new_vote = models.Vote(post_id=data.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "Successfully added"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Message": "Successfully deleted"}
