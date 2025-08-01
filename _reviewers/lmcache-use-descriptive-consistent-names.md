---
title: Use descriptive consistent names
description: Choose names that clearly convey their purpose, role, and meaning while
  maintaining consistency with established patterns in the codebase. Names should
  be self-documenting and unambiguous to future maintainers.
repository: LMCache/LMCache
label: Naming Conventions
language: Python
comments_count: 9
repository_stars: 3800
---

Choose names that clearly convey their purpose, role, and meaning while maintaining consistency with established patterns in the codebase. Names should be self-documenting and unambiguous to future maintainers.

Key principles:
1. **Semantic clarity**: Names should reflect their actual purpose and role in the system architecture. For example, use `receiver_host` instead of `peer_host_name` when the architecture has a clear receiver-sender relationship, or `num_skip_prefix_chunk` instead of `num_skip_chunk` when the meaning is "number of prefix chunks to skip".

2. **Consistency with patterns**: Follow established naming conventions in the codebase. If other batch operations use `batched_xxx` pattern, use `batched_contains` instead of `batch_contains`. Similarly, maintain consistency between related functions like using `batched` instead of mixing `layerwise` and `batched`.

3. **Avoid ambiguous abbreviations**: Use clear variable names instead of cryptic abbreviations. Replace unclear names like `anw` and `anws` with descriptive names like `cache_exists_results`.

4. **Distinguish similar entities**: When multiple files or classes serve similar but distinct purposes, use names that clearly differentiate them. Instead of `disagg_proxy_server.py` and `disagg_proxy_server_original.py`, use names that describe their specific roles.

Example of good naming:
```python
# Instead of:
def batch_contains(self, keys): pass
anws = self.engine_.batched_contains(keys)
for anw in anws:
    if not anw:

# Use:
def batched_contains(self, keys): pass  # Consistent with other batched_xxx methods
cache_exists_results = self.engine_.batched_contains(keys)
for cache_exists in cache_exists_results:
    if not cache_exists:
```