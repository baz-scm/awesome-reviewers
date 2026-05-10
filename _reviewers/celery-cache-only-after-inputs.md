---
title: Cache Only After Inputs
description: When adding or using caching (e.g., @cached_property, sys.modules-dependent
  behavior, or internal resolution caches), ensure the cached value depends only on
  inputs that are already stable.
repository: celery/celery
label: Caching
language: Python
comments_count: 4
repository_stars: 28464
---

When adding or using caching (e.g., @cached_property, sys.modules-dependent behavior, or internal resolution caches), ensure the cached value depends only on inputs that are already stable.

Standard rules:
1) Don’t cache too early
- Avoid accessing a @cached_property inside __init__ if the underlying configuration may still change (or differs between tests). Read from the immediate source of truth (e.g., app.conf) until configuration is finalized, then let caching occur later.

2) Make runtime-dependent caches test-safe
- If behavior depends on module/import state, clear or isolate that state in tests before simulating failures.
- If behavior depends on cached resolution/lookup (e.g., timezone resolution), reset the relevant cache in the test setup.

Example (test isolation for import simulation):
```python
import builtins
from unittest.mock import patch

def failing_import(name, *args, **kwargs):
    if name.startswith('gevent'):
        raise ImportError('Simulated gevent import failure')
    return real_import(name, *args, **kwargs)

real_import = builtins.__import__

with patch.dict('sys.modules', {'gevent': None, 'gevent.monkey': None}):
    with patch('builtins.__import__', side_effect=failing_import):
        result = is_gevent_monkey_patched()
        assert result is False
```

If you can’t guarantee stable inputs or reliable test isolation, prefer non-cached access (or provide explicit cache invalidation hooks) rather than relying on implicit caching side effects.