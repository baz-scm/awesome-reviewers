---
title: Cache expensive computations
description: Identify expensive operations that may be called multiple times and implement
  appropriate caching mechanisms to avoid redundant computation. Use `@cached_property`
  for class properties that involve expensive calculations, store expensive method
  calls in local variables when used repeatedly in loops, and consider memoization
  for frequently accessed data that...
repository: python-poetry/poetry
label: Performance Optimization
language: Python
comments_count: 4
repository_stars: 33496
---

Identify expensive operations that may be called multiple times and implement appropriate caching mechanisms to avoid redundant computation. Use `@cached_property` for class properties that involve expensive calculations, store expensive method calls in local variables when used repeatedly in loops, and consider memoization for frequently accessed data that doesn't change during execution.

Examples of expensive operations to cache:
- File I/O operations like reading configuration files
- Property calculations that iterate over collections
- System information gathering
- Method calls inside loops that return the same result

```python
# Instead of recalculating expensive properties in loops:
for item in items:
    if self.option("top-level") and not any(
        locked.is_same_package_as(r) for r in root.all_requires
    ):
        # expensive calls repeated for each item

# Store expensive calculations outside the loop:
is_top_level = self.option("top-level")
all_requires = root.all_requires
for item in items:
    if is_top_level and not any(
        locked.is_same_package_as(r) for r in all_requires
    ):
        # cached values used efficiently

# Use @cached_property for expensive file operations:
@cached_property
def includes_system_site_packages(self) -> bool:
    pyvenv_cfg = self._path / "pyvenv.cfg"
    return "include-system-site-packages = true" in pyvenv_cfg.read_text()
```

This optimization prevents redundant work and can significantly improve performance, especially in loops or frequently called code paths.