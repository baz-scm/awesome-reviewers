---
title: Deterministic selection parsing
description: When implementing algorithmic “pick/keep/max” logic, make the selected
  set deterministic and the ordering explicit—then compute sort/max keys using robust
  parsing.
repository: karpathy/nanochat
label: Algorithms
language: Python
comments_count: 3
repository_stars: 53189
---

When implementing algorithmic “pick/keep/max” logic, make the selected set deterministic and the ordering explicit—then compute sort/max keys using robust parsing.

Apply:
- Filter at the source: if a category (e.g., val shard) must never be in a selection, exclude it during construction rather than appending then removing.
- Avoid redundant de-dup/sort: if the list you start with (e.g., `range(n)`) is already unique and ordered, don’t add `set()` or extra `sorted()` just to satisfy uniqueness.
- Use reliable key extraction for maxima: prefer `Path`/`stem`/`name` and direct `stat().st_mtime` for sort keys; keep parsing aligned with how files are named/saved.

Example (ids construction and checkpoint step selection):
```python
# Deterministic, minimal ordering
ids_to_download = list(range(num))
if VAL_SHARD_INDEX not in ids_to_download:
    ids_to_download.append(VAL_SHARD_INDEX)
    ids_to_download.sort()  # only if you must re-establish order

# Robust parsing + max selection
checkpoint_files = list(checkpoint_dir.glob('model_*.pt'))
last_step = int(max(f.stem.split('_')[-1] for f in checkpoint_files))
```