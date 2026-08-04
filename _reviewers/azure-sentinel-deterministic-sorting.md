---
title: Deterministic sorting
description: When your code builds collections or performs comparisons, normalize
  inputs to a consistent representation and enforce a deterministic order before iterating/outputting.
repository: Azure/Azure-Sentinel
label: Algorithms
language: Python
comments_count: 2
repository_stars: 6042
---

When your code builds collections or performs comparisons, normalize inputs to a consistent representation and enforce a deterministic order before iterating/outputting.

Apply this to:
- Deduped lists: sort after removing duplicates so file generation/outputs don’t differ between local runs and CI.
- Structured comparisons (e.g., versions): parse and normalize to fixed-length tuples so `1.2` compares equal to `1.2.0`.

Example patterns:

```python
# Deduplicate + deterministic order
unique = list(dict.fromkeys(files))
unique.sort()

# Normalized version comparison
def parse_version(v: str):
    parts = [int(x) for x in v.split('.')]
    return tuple(parts + [0] * (3 - len(parts)))  # pad to 3 components

# (Optionally) also handle longer inputs explicitly if your rules require it.
```