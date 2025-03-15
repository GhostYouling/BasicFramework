from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional
from models.user import RoleEnum

class UserBase(BaseModel):
    email: str  # 改为普通字符串来避免EmailStr验证
    name: str

class UserCreate(UserBase):
    password: str
    role: Optional[RoleEnum] = RoleEnum.user

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None

    class Config:
        from_attributes = True  # 替换 orm_mode

class User(UserBase):
    id: int
    role: RoleEnum
    status: bool

    class Config:
        from_attributes = True  # 替换 orm_mode

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None