from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime

from models.candidate import Candidate
from schemas.candidate import CandidateCreate, Candidate as CandidateSchema
from lib.db import get_crud

# 创建CRUD操作实例
candidate_crud = get_crud(Candidate)


async def create_candidate(db: AsyncSession, candidate: CandidateCreate) -> Candidate:
    """创建候选人"""
    return await candidate_crud.create(db, candidate.model_dump())

async def get_candidates(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    uuid: Optional[str] = None
) -> List[Candidate]:
    """获取候选人列表"""
    filters = {Candidate.uuid == uuid} if uuid else None
    return await candidate_crud.get_multi(db, skip=skip, limit=limit, filters=filters)

async def get_candidate(db: AsyncSession, candidate_id: int) -> Optional[Candidate]:
    """获取单个候选人"""
    return await candidate_crud.get(db, candidate_id)

async def get_candidate_by_uuid(db: AsyncSession, uuid: str) -> Optional[Candidate]:
    """通过UUID获取候选人"""
    filters = {Candidate.uuid == uuid}
    result = await candidate_crud.get_by_filters(db, filters=filters, limit=1)
    return result[0] if result else None

async def update_candidate(
    db: AsyncSession,
    candidate_id: int,
    candidate_data: dict
) -> Optional[Candidate]:
    """更新候选人信息"""
    return await candidate_crud.update(db, id=candidate_id, obj_in=candidate_data)

async def delete_candidate(db: AsyncSession, candidate_id: int) -> bool:
    """删除候选人"""
    result = await candidate_crud.remove(db, candidate_id)
    return result is not None 