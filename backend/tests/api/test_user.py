import pytest
from fastapi import status

def test_create_user(client):
    """测试创建用户"""
    response = client.post("/users/", json={
        "email": "test@example.com",
        "password": "password123",
        "role": "user"
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_login(client):
    """测试用户登录"""
    # 先创建用户
    client.post("/users/", json={
        "email": "test@example.com",
        "password": "password123",
        "role": "user"
    })
    
    # 测试登录
    response = client.post("/token", data={
        "username": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_current_user(client):
    """测试获取当前用户信息"""
    # 先创建用户并登录
    client.post("/users/", json={
        "email": "test@example.com",
        "password": "password123",
        "role": "user"
    })
    
    login_response = client.post("/token", data={
        "username": "test@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]
    
    # 测试获取当前用户
    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "test@example.com" 