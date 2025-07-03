---
title: Respect async execution order
description: When working with asynchronous code, always be mindful of the execution
  order of operations, particularly with regards to yielded dependencies, middleware,
  and background tasks. This affects resource management, error handling, and overall
  application flow.
repository: fastapi/fastapi
label: Concurrency
language: Markdown
comments_count: 4
repository_stars: 86871
---

When working with asynchronous code, always be mindful of the execution order of operations, particularly with regards to yielded dependencies, middleware, and background tasks. This affects resource management, error handling, and overall application flow.

Key considerations:
- Code after `yield` in dependencies runs after middleware completes processing
- For file operations, remember FastAPI executes file methods in a thread pool with proper awaiting
- Always use up-to-date async APIs (e.g., avoid deprecated event loop policies in favor of `asyncio.Runner`)
- Be explicit about execution flow in documentation and comments

Example with yielded dependencies:
```python
async def get_db():
    db = Database()  # This executes when dependency is called
    try:
        yield db  # Flow returns here after dependency is used
    finally:
        # This executes after response is generated and middleware completes
        await db.close()  # Always clean up resources

@app.get("/items/")
async def read_items(db: Database = Depends(get_db)):
    # db is available here from the yield statement above
    return await db.get_items()
```

Understanding async execution order prevents resource leaks, race conditions, and helps ensure proper cleanup even in error scenarios. This is especially important in FastAPI applications where dependencies with `yield` are common for database connections and other resources.