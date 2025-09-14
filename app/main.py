from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
import time
from . import models
from .database import engine, get_db
from . import models


models.Base.metadata.create_all(bind=engine)
app = FastAPI()




load_dotenv()


host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
port = os.getenv("DB_PORT")

class Post(BaseModel):
   title : str
   content : str
   published : bool = True
   year_published : Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host = host, database = database, user = user, password = password, cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Database connection failed")
        print("error was: ", error)
        time.sleep(5)


@app.get("/")
def root():
    return ("{hello : world}")

@app.get("/posts")
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED )
def posts(post: Post, db: Session = Depends(get_db) ):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.get("/posts/{id}")
def post_using_id(id:int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", str(id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found.")   
    return {"data": post}


@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""" , (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found.")
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post : Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    (post.title, post.content, post.published, (str(id))))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found.")
    return {"data": updated_post}

@app.get("/test")
def test(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return {"status": post}

