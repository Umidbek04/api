from pydantic import BaseModel, EmailStr, conint, Field, PydanticUndefinedAnnotation
from typing import Optional
from datetime import datetime
from . import models


class PostBase(BaseModel):

    title: str
    content: str
    published: bool = True
    phone_number: str



class PostMake(PostBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    made_time: datetime

    class Config:
        orm = True

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    user_id: int
    owner: UserResponse


class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm = True

# class UpdatedPost(BaseModel):





class UserMake(BaseModel):

    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class VoteMake(BaseModel):
    post_id: int
    dir: conint(le=1)

# class VoteCount(BaseModel):
#     post: models.Post
#     vote_count: int

#     class Config:
#         from_attributes = True

