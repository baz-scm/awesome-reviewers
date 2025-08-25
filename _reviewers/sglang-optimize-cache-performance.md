---
title: Optimize cache performance
description: Prioritize cache performance by leveraging proven optimization techniques
  and avoiding performance anti-patterns. Use standard caching decorators like @lru_cache
  for functions that benefit from memoization, implement zero-copy operations when
  moving data between cache layers, and avoid unnecessary operations that degrade
  performance.
repository: sgl-project/sglang
label: Caching
language: Python
comments_count: 4
repository_stars: 17245
---

Prioritize cache performance by leveraging proven optimization techniques and avoiding performance anti-patterns. Use standard caching decorators like @lru_cache for functions that benefit from memoization, implement zero-copy operations when moving data between cache layers, and avoid unnecessary operations that degrade performance.

Key practices:
- Apply @lru_cache decorator to functions with reusable results
- Implement zero-copy techniques for cache data transfers  
- Avoid additional slice operations or data transformations in cache paths
- Choose cache architectures that minimize operational overhead

Example:
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def should_use_flashinfer_cutlass_moe_fp4_allgather():
    # Expensive computation cached automatically
    return compute_moe_config()

# Zero-copy backup for Mooncake backend
if self.is_mooncake_backend():
    # Use zero-copy operations instead of generic page backup
    self.zerocopy_page_backup(operation)
```

This approach ensures cache operations remain performant under load while leveraging battle-tested optimization patterns that reduce computational overhead and memory copying.