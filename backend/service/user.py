from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from models.user import User, RoleEnum
from schemas.user import UserCreate, User as UserSchema, UserUpdate
from lib.auth import get_password_hash, verify_password, create_access_token
from lib.db import get_crud

# 创建用户模型的CRUD操作实例
user_crud = get_crud(User)

async def create_user(db: AsyncSession, user: UserCreate) -> UserSchema:
    """创建新用户"""
    hashed_password = get_password_hash(user.password)
    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "role": user.role if hasattr(user, "role") else RoleEnum.user
    }
    db_user = await user_crud.create(db, user_data)
    return UserSchema.from_orm(db_user)

async def get_user_by_email(db: AsyncSession, email: str) -> UserSchema:
    """通过邮箱获取用户"""
    filters = {User.email == email}
    result = await user_crud.get_by_filters(db, filters=filters, limit=1)
    if result and len(result) > 0:
        return UserSchema.from_orm(result[0])
    return None

async def authenticate_user(db: AsyncSession, email: str, password: str) -> UserSchema:
    """验证用户登录"""
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return None
    return user

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100, filters = None) -> list[UserSchema]:
    """获取用户列表"""
    users = await user_crud.get_multi(db, skip=skip, limit=limit, filters=filters)
    return [UserSchema.from_orm(user) for user in users]

async def get_user(db: AsyncSession, user_id: int) -> UserSchema:
    """获取单个用户"""
    user = await user_crud.get(db, user_id)
    return UserSchema.from_orm(user) if user else None

async def update_user(db: AsyncSession, user_id: int, user_data: dict) -> UserSchema:
    """更新用户信息"""
    # 如果包含密码，需要加密
    if "password" in user_data:
        user_data["password"] = get_password_hash(user_data["password"])
        
    updated_user = await user_crud.update(db, id=user_id, obj_in=user_data)
    return UserSchema.from_orm(updated_user) if updated_user else None

async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """删除用户（软删除）"""
    user = await user_crud.remove(db, user_id)
    return user is not None