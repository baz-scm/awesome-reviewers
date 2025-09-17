---
title: Handle async concurrency properly
description: When writing async endpoints, ensure that long-running CPU-bound operations
  don't block the event loop and that concurrent requests don't conflict over shared
  resources. CPU-bound operations should be offloaded to thread pools using asyncio.run_in_executor()
  or similar mechanisms. Additionally, avoid using predictable file paths or shared
  resources that can...
repository: microsoft/markitdown
label: Concurrency
language: Python
comments_count: 2
repository_stars: 76602
---

When writing async endpoints, ensure that long-running CPU-bound operations don't block the event loop and that concurrent requests don't conflict over shared resources. CPU-bound operations should be offloaded to thread pools using asyncio.run_in_executor() or similar mechanisms. Additionally, avoid using predictable file paths or shared resources that can cause race conditions between concurrent requests.

Example of problematic code:
```python
@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    # Problem 1: Blocking CPU-bound operation
    result = markitdown.convert(temp_file_path)  # Blocks event loop
    
    # Problem 2: Race condition with shared file path
    temp_file_path = f"/tmp/{file.filename}"  # Conflicts with concurrent requests
```

Better approach:
```python
@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    # Solution 1: Use thread pool for CPU-bound work
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, markitdown.convert, temp_file_path)
    
    # Solution 2: Use unique file paths
    import uuid
    temp_file_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
```

This prevents blocking the async event loop and eliminates race conditions between concurrent requests.