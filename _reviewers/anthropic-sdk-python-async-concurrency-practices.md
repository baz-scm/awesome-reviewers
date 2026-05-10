---
title: Async Concurrency Practices
description: 'When working in async-capable code, ensure correctness and concurrency
  safety:


  1) Keep async code truly async (no accidental sync calls)

  - If a branch is meant for async transformation, it must call/await async functions
  (e.g., use `await _async_transform_recursive(...)`, not the synchronous equivalent).'
repository: anthropics/anthropic-sdk-python
label: Concurrency
language: Python
comments_count: 4
repository_stars: 3392
---

When working in async-capable code, ensure correctness and concurrency safety:

1) Keep async code truly async (no accidental sync calls)
- If a branch is meant for async transformation, it must call/await async functions (e.g., use `await _async_transform_recursive(...)`, not the synchronous equivalent).

2) Make shared caches/thread-safety explicit
- If you add cached dispatch/lookup tables (or any shared mutable state) that can be hit concurrently, ensure synchronization is in place (or use immutable data / thread-safe initialization patterns).

3) Prevent event-loop blocking from blocking IO
- If code uses libraries that perform blocking IO during “async” operations (e.g., reading AWS config via boto3), either:
  - perform it only once during initialization and reuse results, and/or
  - cache the expensive objects (e.g., a session) so it’s not recreated repeatedly.
- Document the behavior so async users don’t instantiate clients inside hot loops.

Example pattern (bounded blocking + caching):

```py
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def _infer_region() -> str:
    aws_region = os.environ.get("AWS_REGION")
    if aws_region:
        return aws_region

    import boto3  # may do blocking config/FS access
    return boto3.Session().region_name
```

Also ensure parity between sync/async clients: if an async client exposes the same configuration surface as sync, apply the same changes and keep behavior consistent.