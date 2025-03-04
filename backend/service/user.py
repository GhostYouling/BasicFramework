from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.user import User
from backend.schemas.user import UserCreate, User as UserSchema
from backend.lib.auth import get_password_hash, verify_password, create_access_token

async def create_user(db: AsyncSession, user: UserCreate) -> UserSchema:
    hashed_password = get_password_hash(user.password)
    db_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return UserSchema.from_orm(db_user)

async def get_user_by_email(db: AsyncSession, email: str) -> UserSchema:
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    return UserSchema.from_orm(user) if user else None

async def authenticate_user(db: AsyncSession, email: str, password: str) -> UserSchema:
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return None
    return user

async def get_users(db: AsyncSession) -> list[UserSchema]:
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [UserSchema.from_orm(user) for user in users]