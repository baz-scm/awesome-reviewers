---
title: Maintain comprehensive error handling
description: Always preserve and implement thorough error handling that includes proper
  resource cleanup, meaningful logging, and appropriate return values. Don't remove
  existing error handling during code refactoring or simplification.
repository: LMCache/LMCache
label: Error Handling
language: Python
comments_count: 4
repository_stars: 3800
---

Always preserve and implement thorough error handling that includes proper resource cleanup, meaningful logging, and appropriate return values. Don't remove existing error handling during code refactoring or simplification.

Key practices:
1. **Preserve error handling during refactoring** - When simplifying code, maintain existing try-catch blocks and error recovery logic
2. **Clean up resources on failure** - Always free allocated memory, close connections, or reset state when operations fail
3. **Choose appropriate error responses** - Return sensible defaults (like False) instead of throwing exceptions when callers can handle the failure gracefully
4. **Log exceptions with context** - Include meaningful error messages and context when catching exceptions

Example of proper error handling preservation:
```python
# Good - maintains error handling even when simplifying
try:
    return self.connection.exists_sync(key)
except Exception as e:
    with self.lock:
        self.connection = None
        self.failure_time = time.time()
    logger.warning(f"Remote connection failed in contains: {e}")
    logger.warning("Returning False")
    return False

# Bad - removes error handling during simplification
return self.connection.exists_sync(key)
```

This approach prevents silent failures, resource leaks, and provides better debugging information when issues occur.