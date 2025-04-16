import pytest
import aiohttp
import uuid
from datetime import datetime
from typing import Dict, Any

def generate_test_data():
    """生成测试数据，每次调用都会生成新的UUID"""
    return {
        "uuid": str(uuid.uuid4()),
        "job_id": str(uuid.uuid4()),
        "name": "测试候选人",
        "gender": "男",
        "age": "28",
        "education": "本科",
        "education_detail": [
            {
                "school": "测试大学",
                "period": "2015-2019",
                "degree": "计算机科学与技术"
            }
        ],
        "location": "北京",
        "expectation": "期望薪资20k-30k",
        "skills": ["Python", "FastAPI", "SQLAlchemy"],
        "work_experiences": [
            {
                "company": "测试公司",
                "period": "2019-2023",
                "position": "高级工程师",
                "industry": "互联网",
                "subordinates": "5人",
                "salary": "25k",
                "job_category": "后端开发",
                "responsibility": "负责系统架构设计和开发"
            }
        ],
        "detail_link": "http://test.com/candidate/001",
        "detail_extracted": True,
        "is_approved_by_llm": False
    }

@pytest.mark.asyncio
async def test_create_candidate():
    """测试创建候选人"""
    test_data = generate_test_data()
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:8000/api/candidates/",
            json=test_data,
            headers={"Authorization": "Bearer test_token"}
        ) as response:
            assert response.status == 200
            data = await response.json()
            assert data["uuid"] == test_data["uuid"]
            assert data["job_id"] == test_data["job_id"]
            assert data["name"] == test_data["name"]
            assert data["is_approved_by_llm"] == test_data["is_approved_by_llm"]
            assert "id" in data

@pytest.mark.asyncio
async def test_create_duplicate_candidate_same_job():
    """测试在同一岗位下创建重复UUID的候选人"""
    test_data = generate_test_data()
    async with aiohttp.ClientSession() as session:
        # 先创建一个候选人
        await session.post(
            "http://localhost:8000/api/candidates/",
            json=test_data,
            headers={"Authorization": "Bearer test_token"}
        )
        
        # 尝试创建相同UUID和job_id的候选人
        async with session.post(
            "http://localhost:8000/api/candidates/",
            json=test_data,
            headers={"Authorization": "Bearer test_token"}
        ) as response:
            assert response.status == 400
            data = await response.json()
            assert "已存在" in data["detail"]

@pytest.mark.asyncio
async def test_create_candidate_different_job():
    """测试在不同岗位下创建相同UUID的候选人"""
    test_data = generate_test_data()
    async with aiohttp.ClientSession() as session:
        # 先创建一个候选人
        await session.post(
            "http://localhost:8000/api/candidates/",
            json=test_data,
            headers={"Authorization": "Bearer test_token"}
        )
        
        # 创建相同UUID但不同job_id的候选人
        different_job_data = test_data.copy()
        different_job_data["job_id"] = str(uuid.uuid4())
        
        async with session.post(
            "http://localhost:8000/api/candidates/",
            json=different_job_data,
            headers={"Authorization": "Bearer test_token"}
        ) as response:
            assert response.status == 200
            data = await response.json()
            assert data["uuid"] == test_data["uuid"]
            assert data["job_id"] == different_job_data["job_id"]

@pytest.mark.asyncio
async def test_get_candidates_by_job_id():
    """测试按岗位ID获取候选人列表"""
    test_data1 = generate_test_data()
    test_data2 = generate_test_data()
    test_data2["job_id"] = test_data1["job_id"]  # 使用相同的job_id
    
    async with aiohttp.ClientSession() as session:
        # 创建两个相同岗位的候选人
        await session.post(
            "http://localhost:8000/api/candidates/",
            json=test_data1,
            headers={"Authorization": "Bearer test_token"}
        )
        await session.post(
            "http://localhost:8000/api/candidates/",
            json=test_data2,
            headers={"Authorization": "Bearer test_token"}
        )
        
        # 获取特定岗位的候选人
        async with session.get(
            f"http://localhost:8000/api/candidates/?job_id={test_data1['job_id']}",
            headers={"Authorization": "Bearer test_token"}
        ) as response:
            assert response.status == 200
            data = await response.json()
            assert len(data) == 2
            assert all(c["job_id"] == test_data1["job_id"] for c in data)

@pytest.mark.asyncio
async def test_update_candidate_llm_status():
    """测试更新候选人的大模型筛选状态"""
    test_data = generate_test_data()
    async with aiohttp.ClientSession() as session:
        # 先创建一个候选人
        async with session.post(
            "http://localhost:8000/api/candidates/",
            json=test_data,
            headers={"Authorization": "Bearer test_token"}
        ) as create_response:
            candidate_id = (await create_response.json())["id"]
        
        # 更新大模型筛选状态
        update_data = {
            "is_approved_by_llm": True
        }
        async with session.put(
            f"http://localhost:8000/api/candidates/{candidate_id}",
            json=update_data,
            headers={"Authorization": "Bearer test_token"}
        ) as response:
            assert response.status == 200
            data = await response.json()
            assert data["is_approved_by_llm"] == True

@pytest.mark.asyncio
async def test_get_candidates():
    """测试获取候选人列表"""
    test_data = generate_test_data()
    async with aiohttp.ClientSession() as session:
        # 先创建一个候选人
        async with session.post(
            "http://localhost:8000/api/candidates/",
            json=test_data,
            headers={"Authorization": "Bearer test_token"}
        ) as create_response:
            candidate_id = (await create_response.json())["id"]
        
        # 获取候选人列表
        async with session.get(
            "http://localhost:8000/api/candidates/",
            headers={"Authorization": "Bearer test_token"}
        ) as response:
            assert response.status == 200
            data = await response.json()
            assert len(data) > 0
            assert any(c["id"] == candidate_id for c in data)

@pytest.mark.asyncio
async def test_get_candidate():
    """测试获取单个候选人"""
    test_data = generate_test_data()
    async with aiohttp.ClientSession() as session:
        # 先创建一个候选人
        async with session.post(
            "http://localhost:8000/api/candidates/",
            json=test_data,
            headers={"Authorization": "Bearer test_token"}
        ) as create_response:
            candidate_id = (await create_response.json())["id"]
        
        # 获取单个候选人
        async with session.get(
            f"http://localhost:8000/api/candidates/{candidate_id}",
            headers={"Authorization": "Bearer test_token"}
        ) as response:
            assert response.status == 200
            data = await response.json()
            assert data["id"] == candidate_id
            assert data["name"] == test_data["name"]

@pytest.mark.asyncio
async def test_update_candidate():
    """测试更新候选人"""
    test_data = generate_test_data()
    async with aiohttp.ClientSession() as session:
        # 先创建一个候选人
        async with session.post(
            "http://localhost:8000/api/candidates/",
            json=test_data,
            headers={"Authorization": "Bearer test_token"}
        ) as create_response:
            candidate_id = (await create_response.json())["id"]
        
        # 更新候选人信息
        update_data = {
            "name": "更新后的名字",
            "age": "29"
        }
        async with session.put(
            f"http://localhost:8000/api/candidates/{candidate_id}",
            json=update_data,
            headers={"Authorization": "Bearer test_token"}
        ) as response:
            assert response.status == 200
            data = await response.json()
            assert data["name"] == update_data["name"]
            assert data["age"] == update_data["age"]

@pytest.mark.asyncio
async def test_delete_candidate():
    """测试删除候选人"""
    test_data = generate_test_data()
    async with aiohttp.ClientSession() as session:
        # 先创建一个候选人
        async with session.post(
            "http://localhost:8000/api/candidates/",
            json=test_data,
            headers={"Authorization": "Bearer test_token"}
        ) as create_response:
            candidate_id = (await create_response.json())["id"]
        
        # 删除候选人
        async with session.delete(
            f"http://localhost:8000/api/candidates/{candidate_id}",
            headers={"Authorization": "Bearer test_token"}
        ) as response:
            assert response.status == 200
        
        # 验证候选人已被删除
        async with session.get(
            f"http://localhost:8000/api/candidates/{candidate_id}",
            headers={"Authorization": "Bearer test_token"}
        ) as response:
            assert response.status == 404 