---
title: Budget-Aware Performance
description: When code builds prompts, traverses trees, calls external APIs, or processes
  many items, make performance predictable by enforcing budgets, preventing pathological
  inputs, and removing redundant work.
repository: the-pr-agent/pr-agent
label: Performance Optimization
language: Python
comments_count: 7
repository_stars: 12523
---

When code builds prompts, traverses trees, calls external APIs, or processes many items, make performance predictable by enforcing budgets, preventing pathological inputs, and removing redundant work.

Apply these rules:
1) Short-circuit expensive work at global caps
- If there’s a per-request/per-PR budget (tokens, items, characters), stop as soon as the combined total hits the cap.
- Also avoid constructing API clients/workflows when you already know the cap is reached.

Example pattern:

```python
# Assume MAX_ITEMS and items already collected
if len(items) >= MAX_ITEMS:
    return items  # do not build clients or call more APIs

for candidate in candidates:
    if len(items) >= MAX_ITEMS:
        break
    items.append(candidate)
```

2) Guard resource usage with hard limits
- Before reading/parsing/adding content, estimate size and skip inputs that are too large (with a warning log).

3) Reuse fetched data; avoid redundant API calls
- If you already call `get_comments()` once, don’t call `get_comment(comment_id)` again—filter from the in-memory list.

4) Avoid repeated expensive lookups and unnecessary allocations
- Cache `settings = get_settings()` in a local variable when used multiple times.
- Reuse existing provider instances rather than creating new ones inside loops.

5) Prefer O(1) lookups with the right data structures
- Replace repeated `list.index()` inside loops with a dict map.

Net effect: fewer external calls, less parsing/IO, bounded memory, and deterministic latency under worst-case inputs.