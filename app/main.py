


from fastapi import  FastAPI, Response, status, HTTPException, Depends, APIRouter
from .database import engine, get_db
from . import models, schemas, utils
from .routers import post, user



models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router) 

@app.get("/")
def root():
    return ("{hello : world}")








