from pydantic import BaseModel, EmailStr, Field
from typing import List

# --------------------
# POST SCHEMAS
# --------------------

class PostBase(BaseModel):
    title: str


class PostCreate(PostBase):
    user_id: int
    image_url: str


class PostOutSimple(PostBase):
    id: int

    class Config:
        from_attributes = True


class PostOut(PostBase):
    id: int
    owner_id: int
    image_url : str

    class Config:
        from_attributes = True


# --------------------
# USER SCHEMAS
# --------------------

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


# --------------------
# AUTH SCHEMAS
# --------------------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str