---
title: Explicit None Semantics
description: 'When handling optional/nullable inputs, treat “missing” and “explicitly
  set to None” as different semantic states.


  Practical rules:

  - Provide safe fallbacks at the boundary: if a config/input can be `None`, use a
  default that keeps the value non-null.'
repository: celery/celery
label: Null Handling
language: Python
comments_count: 6
repository_stars: 28464
---

When handling optional/nullable inputs, treat “missing” and “explicitly set to None” as different semantic states.

Practical rules:
- Provide safe fallbacks at the boundary: if a config/input can be `None`, use a default that keeps the value non-null.
  ```python
  task_id_generator = conf.get("task_id_generator", uuid)
  if task_id is None:
      task_id = task_id_generator()
  ```
- Preserve explicit caller/request intent: if APIs accept `time_limit=None` (meaning “explicit”), do not collapse it with “argument omitted”. Resolve defaults only when the caller did not provide a value.
- For override fields where frameworks use class-level defaults, you must detect “was set on the instance” vs “fell back to class default”. Using only `getattr(x, 'field', None)` can be misleading; use presence checks (e.g., `__dict__`) before applying fallback logic.
  ```python
  actual = getattr(req, 'ignore_result', None)
  if isinstance(req, Context) and 'ignore_result' not in req.__dict__:
      actual = None  # treat as “unset” to allow task-level fallback
  ```
- Early-exit on truly-null dependencies to prevent latent exceptions: `if producer is None: return`.
- Avoid mutable defaults for optional dict-like arguments (use `None` and initialize inside the function).