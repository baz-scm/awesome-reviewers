---
title: Safe caching practices
description: 'Apply caching only when it is safe, bounded, and correct:


  1) Avoid unbounded method memoization

  - Don’t use `functools.lru_cache/cache` directly on methods whose arguments can
  grow without a tight bound (risk of memory leaks). If you must cache, use a bounded
  cache (`maxsize=...`) or a different lifecycle.'
repository: langchain-ai/langchain
label: Caching
language: Python
comments_count: 7
repository_stars: 136312
---

Apply caching only when it is safe, bounded, and correct:

1) Avoid unbounded method memoization
- Don’t use `functools.lru_cache/cache` directly on methods whose arguments can grow without a tight bound (risk of memory leaks). If you must cache, use a bounded cache (`maxsize=...`) or a different lifecycle.

2) Invalidate caches on mutation
- If cached values depend on mutable fields, clear the relevant cached state when those fields change (prefer a single “root” cache to invalidate rather than scattered caches).

3) Don’t memoize trivial derivations
- If a computed property is cheap (or already bounded by the object size), prefer computing on demand instead of adding memoization.

4) Ensure cache-related transformations preserve structure
- When applying cache tags/controls to messages, operate at the correct level and don’t change block types/structure unintentionally.

5) Document cached-metric semantics
- If tokens/metrics include cached+non-cached portions, document it and provide breakdown fields where needed.

Example: invalidate cached schema on mutation
```python
# Pseudocode illustrating the pattern
class Tool:
    _SCHEMA_INVALIDATING_FIELDS = {"name", "description"}

    def __init__(self):
        self.__dict__["tool_schema"] = None
        self.__dict__["_inferred_input_schema"] = None

    def __setattr__(self, name, value):
        if name in self._SCHEMA_INVALIDATING_FIELDS:
            # Clear only the caches that depend on these fields
            self.__dict__.pop("tool_schema", None)
            self.__dict__.pop("_inferred_input_schema", None)
        super().__setattr__(name, value)
```

Example: avoid unbounded method `lru_cache`
```python
# Prefer bounded caching or per-instance cached_property when lifecycle is bounded.
# Avoid: @lru_cache on methods where keys can grow without bound.

from functools import cached_property

class Parser:
    @cached_property
    def _compiled_pattern(self):
        import re
        return re.compile(r"\d+\.\s([^\n]+)")
```