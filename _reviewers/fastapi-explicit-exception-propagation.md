---
title: Explicit exception propagation
description: Always be explicit about how exceptions are handled, propagated, and
  recovered from in your code. When catching exceptions, either re-raise them or raise
  appropriate new exceptions to ensure proper error flow through the system.
repository: fastapi/fastapi
label: Error Handling
language: Markdown
comments_count: 3
repository_stars: 86871
---

Always be explicit about how exceptions are handled, propagated, and recovered from in your code. When catching exceptions, either re-raise them or raise appropriate new exceptions to ensure proper error flow through the system.

When using dependencies with `yield`, be particularly careful with exception handling:

```python
async def get_db():
    try:
        db = DBSession()
        yield db  # This value is injected into path operations
    except InternalError as e:
        # Either re-raise the original exception
        raise
        # Or raise a more specific exception
        # raise HTTPException(status_code=500, detail="Database error")
    finally:
        db.close()
```

Without explicitly re-raising exceptions or raising new ones, your application might silently fail or return unexpected 500 errors without proper logging. This is especially important in frameworks like FastAPI where dependency execution order and exception handling patterns greatly impact application behavior.

Format exception-related code with proper backticks in documentation (`HTTPException`, `raise`, `except`) and use technically accurate terminology when describing error flows to ensure other developers correctly understand error handling patterns in your codebase.