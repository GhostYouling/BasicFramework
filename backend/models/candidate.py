from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey, UniqueConstraint
from models.base import BaseModel

class Candidate(BaseModel):
    """候选人表"""
    __tablename__ = "candidate"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(100), index=True)  # 移除unique约束
    job_id = Column(String(100), index=True)  # 岗位编号
    name = Column(String(50))
    gender = Column(String(10))
    age = Column(String(10))
    education = Column(String(50))
    education_detail = Column(JSON)  # 存储教育经历详情列表
    location = Column(String(100))
    expectation = Column(String(200))
    skills = Column(JSON)  # 存储技能列表
    work_experiences = Column(JSON)  # 存储工作经历列表
    detail_link = Column(String(500))
    detail_extracted = Column(Boolean, default=True)
    is_approved_by_llm = Column(Boolean, default=False)  # 是否通过大模型筛选

    __table_args__ = (
        # 添加联合唯一约束，确保同一个候选人在同一个岗位下不会重复
        UniqueConstraint('uuid', 'job_id', name='uix_candidate_uuid_job'),
        {'sqlite_autoincrement': True},
    )