from sqlalchemy import Column, Integer, String, Enum
import enum
from models.base import BaseModel

class RoleEnum(enum.Enum):
    admin = "admin"
    user = "user"

class User(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)