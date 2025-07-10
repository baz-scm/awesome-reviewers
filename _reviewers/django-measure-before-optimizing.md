---
title: Measure before optimizing
description: Always measure performance impact before implementing optimizations and
  focus on changes with meaningful benefits. Python's performance characteristics
  can be unintuitive - optimizations that seem beneficial might have minimal impact,
  while simple changes can yield significant improvements.
repository: django/django
label: Performance Optimization
language: Python
comments_count: 4
repository_stars: 84182
---

Always measure performance impact before implementing optimizations and focus on changes with meaningful benefits. Python's performance characteristics can be unintuitive - optimizations that seem beneficial might have minimal impact, while simple changes can yield significant improvements.

Key optimization patterns to consider:

1. **Cache attribute lookups in loops**:
```python
# Inefficient - repeated attribute lookups
missing_instances = [i for i in instances if not self.field.is_cached(i)]

# Optimized - single lookup cached in local variable
is_cached = self.field.is_cached
missing_instances = [i for i in instances if not is_cached(i)]
```

2. **Avoid expensive operations** like materializing entire stack traces with `inspect.stack()`. Use targeted approaches instead:
```python
# Expensive - materializes all stack frames
if "aggregate" in {frame.function for frame in inspect.stack()}:
    # ...

# More efficient - only access needed frames
frame = inspect.currentframe()
for _ in range(5):
    try:
        frame = frame.f_back
    except AttributeError:
        break
else:
    is_aggregate = 'aggregate' in frame.function
del frame  # Avoid reference cycles
```

3. **Know your standard library operations**. For dictionary filtering, `copy()` and `pop()` can be more efficient than comprehensions:
```python
# ~110ns
p = params.copy()
p.pop("q", None)

# ~240ns
{k: v for k, v in params.items() if k != "q"}
```

Always confirm your optimizations with timings (using `timeit` or similar tools) on representative data volumes to ensure the changes provide meaningful benefits.