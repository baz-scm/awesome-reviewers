---
title: Optimize IO with async
description: FastAPI's performance advantage comes from its asynchronous foundation
  built on Starlette and Uvicorn, using `uvloop` which is significantly faster than
  Python's default asyncio implementation. To maximize application performance, use
  asynchronous programming patterns for IO-bound operations such as database queries,
  API requests, and file operations.
repository: fastapi/fastapi
label: Performance Optimization
language: Markdown
comments_count: 2
repository_stars: 86871
---

FastAPI's performance advantage comes from its asynchronous foundation built on Starlette and Uvicorn, using `uvloop` which is significantly faster than Python's default asyncio implementation. To maximize application performance, use asynchronous programming patterns for IO-bound operations such as database queries, API requests, and file operations.

Converting blocking operations to async versions prevents the server from stalling while waiting for external resources, allowing it to handle more concurrent requests:

```python
# Less efficient - blocks the server while waiting for response
@app.get("/external-data/")
def get_external_data():
    response = requests.get("https://api.example.com/data")
    data = response.json()
    return {"result": data}

# More efficient - releases the event loop while waiting
@app.get("/external-data/")
async def get_external_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        data = response.json()
    return {"result": data}
```

For CPU-bound operations that can't be made asynchronous, consider running FastAPI with multiple workers to utilize all available CPU cores:

```bash
uvicorn app:app --workers 4
```

This deployment strategy improves throughput for high-traffic applications while maintaining FastAPI's performance benefits.