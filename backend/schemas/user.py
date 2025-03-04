from pydantic import BaseModel
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: RoleEnum

    class Config:
        orm_mode = True  # 支持从 SQLAlchemy ORM 对象转换

class Token(BaseModel):
    access_token: str
    token_type: str