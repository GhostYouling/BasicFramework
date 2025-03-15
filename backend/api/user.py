from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Set
from sqlalchemy.sql.expression import BinaryExpression

from lib.auth import create_access_token, get_current_user
from database import AsyncSessionLocal
from service.user import (
    create_user, authenticate_user, get_users, get_user, 
    update_user, delete_user
)
from models.user import User, RoleEnum
from schemas.user import UserCreate, UserUpdate, User as UserSchema, Token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/users/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """创建新用户"""
    return await create_user(db, user)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """用户登录获取token"""
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="邮箱或密码不正确",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/", response_model=list[UserSchema])
async def read_users(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=100),
    role: Optional[RoleEnum] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    """获取用户列表，可选按角色过滤"""
    # 检查权限 - 只有管理员可以查看所有用户
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限执行此操作"
        )
    
    filters = set()
    if role:
        filters.add(User.role == role)
    
    return await get_users(db, skip=skip, limit=limit, filters=filters)

@router.get("/users/{user_id}", response_model=UserSchema)
async def read_user(
    user_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    """获取单个用户详情"""
    # 检查权限 - 用户只能查看自己的信息，管理员可以查看所有
    if current_user.role != RoleEnum.admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限查看其他用户信息"
        )
        
    user = await get_user(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return user

@router.put("/users/{user_id}", response_model=UserSchema)
async def update_user_endpoint(
    user_id: int = Path(..., ge=1),
    user_data: UserUpdate = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    """更新用户信息"""
    # 检查权限 - 用户只能更新自己的信息，管理员可以更新所有
    if current_user.role != RoleEnum.admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限更新其他用户信息"
        )
    
    # 转换为字典
    user_dict = user_data.dict(exclude_unset=True)
    
    updated_user = await update_user(db, user_id, user_dict)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return updated_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(
    user_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    """删除用户（软删除）"""
    # 检查权限 - 只有管理员可以删除用户
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限执行此操作"
        )
    
    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return None

@router.get("/me", response_model=UserSchema)
async def read_current_user(current_user: UserSchema = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return current_user