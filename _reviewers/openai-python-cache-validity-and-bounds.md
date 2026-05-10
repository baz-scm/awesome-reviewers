---
title: Cache validity and bounds
description: 'When adding caching, ensure **(1) correctness via validity/refresh**
  and **(2) safety via bounds/staleness resistance**.


  ### 1) Align cache lifetime with real validity'
repository: openai/openai-python
label: Caching
language: Python
comments_count: 5
repository_stars: 30731
---

When adding caching, ensure **(1) correctness via validity/refresh** and **(2) safety via bounds/staleness resistance**.

### 1) Align cache lifetime with real validity
- For tokens/credentials, cached values must not outlive the underlying credential/session window.
- Prefer conservative defaults and refresh **before** expiry (e.g., refresh at ~90% of TTL or `TTL - margin`).

```python
def token_provider(*, token_duration: int = 3600):
    _cached = [None]
    _refresh_at = [0.0]

    def generate() -> str:
        # local signing; no network
        return "bedrock-api-key-..."

    def get() -> str:
        import time
        now = time.monotonic()
        if _cached[0] is None or now >= _refresh_at[0]:
            _cached[0] = generate()
            _refresh_at[0] = now + max(token_duration - 60, token_duration * 0.9)
        return _cached[0]

    return get
```

### 2) Prevent unbounded memory growth
- If cache keys can grow with user input/model identity, do **not** use unbounded caches.
- Use a bounded strategy (e.g., `functools.lru_cache(maxsize=...)`) or a bounded LRU/size-capped cache.
- For caches intended to rely on GC (e.g., weak references), verify that your keying strategy doesn’t keep references alive indefinitely under typical usage.

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_type_adapter(type_):
    # expensive instantiation avoided
    return make_adapter(type_)
```

### 3) Don’t cache derived auth/state that can go stale
- If cached results depend on mutable client fields (e.g., `api_key`), either:
  - invalidate/update the cache when those inputs change, or
  - avoid caching derived values that might mismatch current state.

### Checklist
- Does the cached value have a real external validity window? If yes, is TTL/refresh tied to it (and conservative)?
- Can the cache key cardinality grow without bound? If yes, add bounds (max size) and/or adjust key strategy.
- Can cached outputs become inconsistent when configuration changes? If yes, ensure invalidation or remove the caching assumption.