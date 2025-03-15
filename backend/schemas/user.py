from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional
from models.user import RoleEnum

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str
    role: Optional[RoleEnum] = RoleEnum.user

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None

    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    role: RoleEnum
    status: bool

    class Config:
        orm_mode = True  # 支持从 SQLAlchemy ORM 对象转换

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None