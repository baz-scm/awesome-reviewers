---
title: Explicit config behavior
description: 'Ensure configuration behavior is predictable, validated, and migration-friendly:


  - Precedence: When combining env vars, settings, and defaults, explicitly define
  and implement the precedence order (and document/announce any change). Avoid “surprising”
  priority flips.'
repository: celery/celery
label: Configurations
language: Python
comments_count: 8
repository_stars: 28464
---

Ensure configuration behavior is predictable, validated, and migration-friendly:

- Precedence: When combining env vars, settings, and defaults, explicitly define and implement the precedence order (and document/announce any change). Avoid “surprising” priority flips.
- Defaults & transitions: Choose defaults for backward compatibility, but provide a clear deprecation/transition plan for behavior changes. For feature flags, minimize error-prone user responsibility—prefer safe/automatic behavior when possible, and document operational warnings.
- Config schema: Add new options to the formal defaults/conf schema and then access them directly (avoid optional `get()` patterns when the option is already defined).
- Validation: Validate config values and fail fast for invalid/misconfigured settings (raise `ImproperlyConfigured` rather than using silent fallbacks). If a setting is expected to be callable/type-specific, check it.

Example (fail-fast validation for a config-provided function):
```python
from celery.exceptions import ImproperlyConfigured

repr_function = self.app.conf.task_args_repr_function
if not repr_function:
    raise ImproperlyConfigured("task_args_repr_function must be set")
if isinstance(repr_function, str):
    # resolve symbol_by_name(...)
    repr_function = symbol_by_name(repr_function)
if not callable(repr_function):
    raise ImproperlyConfigured("task_args_repr_function must be callable")
```

Example (explicit precedence):
- Decide whether `broker_url` or `CELERY_BROKER_*_URL` wins, implement that order consistently, and ensure it’s documented as a behavior contract.
