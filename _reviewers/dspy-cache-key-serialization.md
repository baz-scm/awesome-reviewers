---
title: Cache key serialization
description: When implementing caching for functions that accept complex objects (dictionaries
  with mixed types, Pydantic models, callables), ensure proper cache key generation
  by filtering out non-serializable objects and converting complex types to serializable
  formats.
repository: stanfordnlp/dspy
label: Caching
language: Python
comments_count: 3
repository_stars: 27813
---

When implementing caching for functions that accept complex objects (dictionaries with mixed types, Pydantic models, callables), ensure proper cache key generation by filtering out non-serializable objects and converting complex types to serializable formats.

Key requirements:
1. **Filter out callables**: Exclude callable objects from cache key generation as they cannot be reliably serialized or hashed
2. **Convert Pydantic models**: Transform Pydantic BaseModel instances to dictionaries using `.dict()` or `.schema()` methods
3. **Use consistent serialization**: Apply deterministic JSON serialization with sorted keys for reliable cache key generation

Example implementation:
```python
def cache_key(request: Dict[str, Any]) -> str:
    # Transform Pydantic models and exclude unhashable objects
    params = {
        k: (v.dict() if isinstance(v, pydantic.BaseModel) else v) 
        for k, v in request.items() 
        if not callable(v)
    }
    return sha256(ujson.dumps(params, sort_keys=True).encode()).hexdigest()
```

This approach prevents serialization errors like "TypeError: <class> is not JSON serializable" and ensures cache keys remain consistent across different execution contexts. The pattern is essential for caching LLM requests, embedding calls, and other functions that accept complex parameter objects.