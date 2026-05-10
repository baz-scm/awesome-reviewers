---
title: Avoid Hidden Performance Traps
description: 'Default rule: in performance-sensitive code, prevent hidden blowups
  and avoid expensive work being executed repeatedly in hot paths or on import.


  Apply this checklist:'
repository: langchain-ai/langchain
label: Performance Optimization
language: Python
comments_count: 5
repository_stars: 136312
---

Default rule: in performance-sensitive code, prevent hidden blowups and avoid expensive work being executed repeatedly in hot paths or on import.

Apply this checklist:
1) Replace inefficient primitives inside loops
- Watch for patterns like `pop(0)` or `sort()` on each iteration.
- Use `collections.deque` or `heapq` where applicable.

2) Don’t do global scans per iteration in graph/ordering logic
- If you’re performing a topological sort / dependency resolution, build a reverse-dependency adjacency list so each “removed node” updates only its affected neighbors.

3) Cache expensive introspection/metadata
- If you use reflection (e.g., `inspect.signature`) or other typing-introspection, compute it once when wiring middleware/handlers, store it, and reuse it during request processing.

4) Prefer lazy, memoized loading over eager initialization
- Avoid doing heavy imports/provider setup in `__init__` paths; delay until actually needed and memoize results.

5) Choose fast strategies by default (when the API is designed for it)
- For token counting/estimation, prefer approximate fast paths unless exact/model-accurate counts are required.

Example (dependency resolution):
```python
from collections import deque

# Build reverse deps once: dep -> set(dependents)
reverse_deps = {}
for cls, deps in dep_graph.items():
    for dep in deps:
        reverse_deps.setdefault(dep, set()).add(cls)

queue = deque(sorted([c for c in instance_by_class if in_degree[c] == 0], key=lambda x: x.__name__))
while queue:
    current = queue.popleft()
    for dependent in reverse_deps.get(current, ()):  # only affected neighbors
        in_degree[dependent] -= 1
        if in_degree[dependent] == 0:
            queue.append(dependent)
```