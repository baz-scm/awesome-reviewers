---
title: Correct Pagination Ordering
description: Ensure algorithmic results (ordering, counts, and pagination) remain
  correct after filtering/slicing and that sorting/dedup logic is both efficient and
  deterministic.
repository: awslabs/mcp
label: Algorithms
language: Python
comments_count: 4
repository_stars: 9545
---

Ensure algorithmic results (ordering, counts, and pagination) remain correct after filtering/slicing and that sorting/dedup logic is both efficient and deterministic.

Practical rules:
1) Order/recency claims must match the actual data returned
- If you only fetch a partial subset (e.g., `MaxKeys=10`), you cannot claim “newest-first” unless the subset is actually chosen by recency.
- Either change the fetch strategy or adjust the output wording to avoid misleading semantics.

2) Returned totals must reflect what the caller truly receives
- If you fetch extra results and then filter/slice client-side, recompute the effective `total` based on the post-processed result set (e.g., return `len(docs)` rather than a pre-filter server count).

3) Dedup must be hash-based and collision-safe
- Avoid `result_copy not in results` style membership checks (quadratic + projection collisions).
- Track seen identifiers in a `set` (prefer stable IDs like `slug`).

4) Sorting keys must define a total order
- Never return mixed-type sort keys (`int` vs `str`) from the same comparator.
- Use a tuple-based key with a type/group discriminator.

Example patterns:

Dedup with `set`:
```python
limit = 10
seen_slugs: set[str] = set()
results = []

for m in all_matches:
    slug = m.get('slug', '')
    if slug in seen_slugs:
        continue
    seen_slugs.add(slug)
    results.append({k: v for k, v in m.items() if k != 'tags'})
    if len(results) >= limit:
        break
```

Total-order sort key (mixed numeric/non-numeric):
```python
def line_key(k: str):
    return (0, int(k), '') if k.isdigit() else (1, 0, k)

sorted_line_numbers = sorted(line_numbers, key=line_key)
```
