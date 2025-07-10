---
title: Async resource cleanup guarantees
description: When implementing async context managers, always ensure proper resource
  cleanup even during task cancellation. Use try/finally blocks to guarantee that
  resources are released and context state is properly restored regardless of how
  execution terminates.
repository: django/django
label: Concurrency
language: Python
comments_count: 3
repository_stars: 84182
---

When implementing async context managers, always ensure proper resource cleanup even during task cancellation. Use try/finally blocks to guarantee that resources are released and context state is properly restored regardless of how execution terminates.

Consider this flawed implementation:

```python
async def __aexit__(self, exc_type, exc_value, traceback):
    # This may never complete if a CancelledError is raised
    await self.connection.aclose()
    await self.cleanup_state()
```

If a task is cancelled while in this context, `aclose()` might never be called, leading to connection leaks and inconsistent state. Instead, implement:

```python
async def __aexit__(self, exc_type, exc_value, traceback):
    try:
        # Handle normal cleanup first
        if not exc_type:
            await self.connection.acommit()
        else:
            await self.connection.arollback()
    finally:
        # Always execute these operations, even during cancellation
        await self.connection.aclose()
        await self.cleanup_state()
```

This pattern ensures that critical cleanup operations always execute, preventing resource leaks when tasks are cancelled. When working with resource pools or connection stacks, this approach is essential to maintain system integrity and prevent gradual resource exhaustion.

Additionally, use distinct naming for async methods (like `aclose` vs `close`) rather than overloading, to avoid confusing errors and make debugging easier when async/sync boundaries are crossed incorrectly.