from fastapi import  FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas,utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db) ):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user

@router.get("/{id}", response_model= schemas.UserResponse)
def user_using_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"user with id: {id} was not found.")   
    return user

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"user with id: {id} was not found.")
    user.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= schemas.UserResponse)
def update_user(id: int, updated_user : schemas.CreateUser, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"user with id: {id} was not found.")
    user_query.update(dict(updated_user), synchronize_session = False)
    db.commit()
    return user_query.first() 