from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    created_at: str

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    created_at: datetime
    