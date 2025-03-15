from typing import TypeVar, Generic, Type, List, Optional, Any, Dict, Union, Set
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import BinaryExpression
from datetime import datetime

from backend.models.base import BaseModel

T = TypeVar('T', bound=BaseModel)

class CRUDBase(Generic[T]):
    def __init__(self, model: Type[T]):
        """
        CRUD 基础类，提供基本的数据库操作
        :param model: 数据模型类
        """
        self.model = model

    async def create(self, db: AsyncSession, obj_in: Dict[str, Any]) -> T:
        """
        创建记录
        :param db: 数据库会话
        :param obj_in: 创建对象的数据
        :return: 创建的对象
        """
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, id: Any, filters: Optional[Set[BinaryExpression]] = None) -> Optional[T]:
        """
        根据ID获取对象（只返回未删除的对象）
        :param db: 数据库会话
        :param id: 对象ID
        :param filters: 可选的额外过滤条件集合
        :return: 查询到的对象或None
        """
        conditions = [
            self.model.id == id,
            self.model.status == True
        ]
        
        # 添加自定义过滤条件
        if filters:
            conditions.extend(filters)
            
        stmt = select(self.model).where(*conditions)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100, filters: Optional[Set[BinaryExpression]] = None
    ) -> List[T]:
        """
        获取多条记录（只返回未删除的对象）
        :param db: 数据库会话
        :param skip: 跳过前几条
        :param limit: 返回最大条数
        :param filters: 可选的额外过滤条件集合
        :return: 对象列表
        """
        conditions = [self.model.status == True]
        
        # 添加自定义过滤条件
        if filters:
            conditions.extend(filters)
            
        stmt = select(self.model).where(*conditions).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def update(
        self, db: AsyncSession, *, id: Any, obj_in: Union[Dict[str, Any], T], filters: Optional[Set[BinaryExpression]] = None
    ) -> Optional[T]:
        """
        更新记录
        :param db: 数据库会话
        :param id: 对象ID
        :param obj_in: 更新的数据
        :param filters: 可选的额外过滤条件集合
        :return: 更新后的对象
        """
        # 先查询对象是否存在且未被删除
        db_obj = await self.get(db, id, filters)
        if not db_obj:
            return None
            
        # 如果obj_in是字典，直接更新
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # 否则转换为字典
            update_data = obj_in.dict(exclude_unset=True)
            
        # 更新对象
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
                
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, id: Any, filters: Optional[Set[BinaryExpression]] = None) -> Optional[T]:
        """
        软删除记录（将status设置为False）
        :param db: 数据库会话
        :param id: 对象ID
        :param filters: 可选的额外过滤条件集合
        :return: 被删除的对象
        """
        db_obj = await self.get(db, id, filters)
        if not db_obj:
            return None
            
        db_obj.status = False
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def hard_remove(self, db: AsyncSession, id: Any, filters: Optional[Set[BinaryExpression]] = None) -> bool:
        """
        硬删除记录（真实从数据库中删除）
        :param db: 数据库会话
        :param id: 对象ID
        :param filters: 可选的额外过滤条件集合
        :return: 删除是否成功
        """
        conditions = [self.model.id == id]
        
        # 添加自定义过滤条件
        if filters:
            conditions.extend(filters)
            
        stmt = delete(self.model).where(*conditions)
        await db.execute(stmt)
        await db.commit()
        return True
        
    async def count(self, db: AsyncSession, filters: Optional[Set[BinaryExpression]] = None) -> int:
        """
        计算有效记录总数（未被删除的）
        :param db: 数据库会话
        :param filters: 可选的额外过滤条件集合
        :return: 记录数
        """
        conditions = [self.model.status == True]
        
        # 添加自定义过滤条件
        if filters:
            conditions.extend(filters)
            
        stmt = select(self.model).where(*conditions)
        result = await db.execute(stmt)
        return len(result.scalars().all())
        
    async def get_by_filters(
        self, db: AsyncSession, *, filters: Set[BinaryExpression], skip: int = 0, limit: int = 100
    ) -> List[T]:
        """
        根据指定的过滤条件获取记录（包含status=True条件）
        :param db: 数据库会话
        :param filters: 过滤条件集合
        :param skip: 跳过前几条
        :param limit: 返回最大条数
        :return: 对象列表
        """
        # 确保添加状态条件
        all_filters = {self.model.status == True}
        all_filters.update(filters)
        
        stmt = select(self.model).where(*all_filters).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()


def get_crud(model: Type[BaseModel]) -> CRUDBase:
    """
    创建CRUD操作类的工厂函数
    :param model: 数据模型类
    :return: 对应的CRUD操作类实例
    """
    return CRUDBase(model) 