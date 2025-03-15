from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class BaseModel(Base):
    __abstract__ = True
    
    status = Column(Boolean, default=True, nullable=False, doc="状态，True为正常，False为删除")
    create_time = Column(DateTime, default=datetime.now, nullable=False, doc="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, doc="更新时间")

    @declared_attr
    def __tablename__(cls):
        """根据类名自动生成表名"""
        return cls.__name__.lower()

# 监听器：在实例创建时设置创建时间和更新时间
@event.listens_for(BaseModel, 'before_insert', propagate=True)
def before_insert(mapper, connection, instance):
    instance.create_time = datetime.now()
    instance.update_time = datetime.now()

# 监听器：在实例更新时设置更新时间
@event.listens_for(BaseModel, 'before_update', propagate=True)
def before_update(mapper, connection, instance):
    instance.update_time = datetime.now() 