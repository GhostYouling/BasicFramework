import pytest

@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def test_token():
    """测试用户token"""
    return "test_token"  # 这里应该使用真实的JWT token生成逻辑 