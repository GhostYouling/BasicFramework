from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from schemas.candidate import Candidate, CandidateCreate
from service.candidate import (
    create_candidate,
    get_candidates,
    get_candidate,
    get_candidate_by_uuid,
    update_candidate,
    delete_candidate
)
from dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Candidate)
async def create_candidate_endpoint(
    candidate: CandidateCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建新的候选人"""
    # 检查UUID是否已存在
    existing_candidate = await get_candidate_by_uuid(db, candidate.uuid)
    if existing_candidate:
        raise HTTPException(status_code=400, detail="UUID已存在")
    
    return await create_candidate(db, candidate)

@router.get("/", response_model=List[Candidate])
async def read_candidates(
    skip: int = 0,
    limit: int = 100,
    uuid: str = None,
    db: AsyncSession = Depends(get_db)
):
    """获取候选人列表"""
    return await get_candidates(db, skip=skip, limit=limit, uuid=uuid)

@router.get("/{candidate_id}", response_model=Candidate)
async def read_candidate(
    candidate_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取单个候选人详情"""
    candidate = await get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    return candidate

@router.put("/{candidate_id}", response_model=Candidate)
async def update_candidate_endpoint(
    candidate_id: int,
    candidate_data: dict,
    db: AsyncSession = Depends(get_db)
):
    """更新候选人信息"""
    updated_candidate = await update_candidate(db, candidate_id, candidate_data)
    if not updated_candidate:
        raise HTTPException(status_code=404, detail="候选人不存在")
    return updated_candidate

@router.delete("/{candidate_id}")
async def delete_candidate_endpoint(
    candidate_id: int,
    db: AsyncSession = Depends(get_db)
):
    """删除候选人"""
    success = await delete_candidate(db, candidate_id)
    if not success:
        raise HTTPException(status_code=404, detail="候选人不存在")
    return {"message": "删除成功"} 