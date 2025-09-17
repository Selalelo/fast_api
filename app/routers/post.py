from fastapi import  FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts 


@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def posts(post: schemas.CreatePost, db: Session = Depends(get_db) ):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post

@router.get("/{id}", response_model= schemas.PostResponse)
def post_using_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found.")   
    return post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found.")
    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/ {id}", response_model= schemas.PostResponse)
def update_post(id: int, updated_post : schemas.CreatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found.")
    post_query.update(dict(updated_post), synchronize_session = False)
    db.commit()
    return post_query.first()

