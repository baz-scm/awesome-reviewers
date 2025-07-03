---
title: Sync versus async tests
description: Choose the appropriate testing approach based on your test requirements.
  For standard API endpoint testing, use `TestClient` with regular functions. For
  tests requiring async operations (like database queries), use `AsyncClient` with
  proper async test configuration.
repository: fastapi/fastapi
label: Testing
language: Markdown
comments_count: 7
repository_stars: 86871
---

Choose the appropriate testing approach based on your test requirements. For standard API endpoint testing, use `TestClient` with regular functions. For tests requiring async operations (like database queries), use `AsyncClient` with proper async test configuration.

**For synchronous tests:**
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

**For asynchronous tests:**
```python
import pytest
import httpx
from app.main import app

@pytest.mark.anyio
async def test_async_operations():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        # Now you can use other async operations
        # await database.fetch_one("SELECT * FROM items")
```

Remember that async tests require additional setup:
1. Install the appropriate pytest plugin (`pytest-anyio` or `pytest-asyncio`)
2. Mark your test functions with the correct decorator
3. Use `async def` for the test function
4. Use `AsyncClient` instead of `TestClient`

This approach ensures your tests can properly interact with both your FastAPI application and any external asynchronous dependencies without blocking or creating concurrency issues.