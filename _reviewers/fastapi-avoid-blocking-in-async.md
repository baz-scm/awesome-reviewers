---
title: Avoid blocking in async
description: When working with asynchronous code, ensure that I/O operations (like
  file reads/writes) don't block the event loop. Blocking operations in async contexts
  can lead to performance degradation, deadlocks, or unexpected behavior.
repository: fastapi/fastapi
label: Concurrency
language: Python
comments_count: 2
repository_stars: 86871
---

When working with asynchronous code, ensure that I/O operations (like file reads/writes) don't block the event loop. Blocking operations in async contexts can lead to performance degradation, deadlocks, or unexpected behavior.

- Use asynchronous alternatives for I/O operations (aiofiles instead of built-in open, etc.)
- If a blocking operation cannot be avoided, consider offloading it to a separate thread

Example:
```python
# Problematic - blocking I/O in async context
async def shutdown_event():
    with open("log.txt", "w") as f:  # Blocking operation
        f.write("Application shutdown")

# Better - using async I/O
import aiofiles
async def shutdown_event():
    async with aiofiles.open("log.txt", "w") as f:
        await f.write("Application shutdown")

# Alternative - offload blocking I/O to a thread
from concurrent.futures import ThreadPoolExecutor
thread_pool = ThreadPoolExecutor()

async def shutdown_event():
    def write_log():
        with open("log.txt", "w") as f:
            f.write("Application shutdown")
    
    await asyncio.get_event_loop().run_in_executor(thread_pool, write_log)
```