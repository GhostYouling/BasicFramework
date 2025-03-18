import pytest
from datetime import datetime
from typing import Dict, Any

# 测试数据
test_candidate_data = {
    "uuid": "test-uuid-001",
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
    "extract_time": datetime.now().isoformat()
}

@pytest.mark.asyncio
async def test_create_candidate(client: Any, test_token: str):
    """测试创建候选人"""
    response = client.post(
        "/api/candidates/",
        json=test_candidate_data,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == test_candidate_data["uuid"]
    assert data["name"] == test_candidate_data["name"]
    assert "id" in data

@pytest.mark.asyncio
async def test_create_duplicate_candidate(client: Any, test_token: str):
    """测试创建重复UUID的候选人"""
    # 先创建一个候选人
    client.post(
        "/api/candidates/",
        json=test_candidate_data,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    
    # 尝试创建相同UUID的候选人
    response = client.post(
        "/api/candidates/",
        json=test_candidate_data,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 400
    assert "UUID已存在" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_candidates(client: Any, test_token: str):
    """测试获取候选人列表"""
    # 先创建一个候选人
    create_response = client.post(
        "/api/candidates/",
        json=test_candidate_data,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    candidate_id = create_response.json()["id"]
    
    # 获取候选人列表
    response = client.get(
        "/api/candidates/",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(c["id"] == candidate_id for c in data)

@pytest.mark.asyncio
async def test_get_candidate(client: Any, test_token: str):
    """测试获取单个候选人"""
    # 先创建一个候选人
    create_response = client.post(
        "/api/candidates/",
        json=test_candidate_data,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    candidate_id = create_response.json()["id"]
    
    # 获取单个候选人
    response = client.get(
        f"/api/candidates/{candidate_id}",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == candidate_id
    assert data["name"] == test_candidate_data["name"]

@pytest.mark.asyncio
async def test_update_candidate(client: Any, test_token: str):
    """测试更新候选人"""
    # 先创建一个候选人
    create_response = client.post(
        "/api/candidates/",
        json=test_candidate_data,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    candidate_id = create_response.json()["id"]
    
    # 更新候选人信息
    update_data = {
        "name": "更新后的名字",
        "age": "29"
    }
    response = client.put(
        f"/api/candidates/{candidate_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["age"] == update_data["age"]

@pytest.mark.asyncio
async def test_delete_candidate(client: Any, test_token: str):
    """测试删除候选人"""
    # 先创建一个候选人
    create_response = client.post(
        "/api/candidates/",
        json=test_candidate_data,
        headers={"Authorization": f"Bearer {test_token}"}
    )
    candidate_id = create_response.json()["id"]
    
    # 删除候选人
    response = client.delete(
        f"/api/candidates/{candidate_id}",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    
    # 验证候选人已被删除
    get_response = client.get(
        f"/api/candidates/{candidate_id}",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert get_response.status_code == 404 