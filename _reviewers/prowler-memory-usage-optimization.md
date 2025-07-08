---
title: Memory usage optimization
description: 'Optimize memory usage in high-performance applications by implementing
  explicit memory management techniques. This includes:


  1. **Configure cache limits** to prevent excessive memory consumption:'
repository: prowler-cloud/prowler
label: Performance Optimization
language: Python
comments_count: 4
repository_stars: 11834
---

Optimize memory usage in high-performance applications by implementing explicit memory management techniques. This includes:

1. **Configure cache limits** to prevent excessive memory consumption:
```python
# Set appropriate cache size limits for database operations
def _configure_cache(self):
    with self.conn:
        self.conn.execute(f'PRAGMA cache_size = {-self.cache_size}')
```

2. **Use context managers for garbage collection** when processing large datasets:
```python
@contextmanager
def force_gc(disable_gc=False):
    if disable_gc:
        gc.disable()
    try:
        yield
    finally:
        gc.collect()
    if disable_gc:
        gc.enable()
```

3. **Process data in streams** rather than loading everything into memory at once:
```python
# Instead of:
all_findings.extend(findings)
# And then processing all findings at once

# Prefer streaming approach:
for finding in findings:
    process_and_write_to_file(finding)
```

These techniques are particularly important for long-running processes, applications handling large datasets, or systems with limited resources.