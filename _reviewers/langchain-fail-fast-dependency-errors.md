---
title: Fail Fast Dependency Errors
description: 'When resolving dependencies or other derived configuration, never “log-and-continue”
  into an inconsistent internal state.


  Apply this standard:

  1. **Validate at the source (fail fast):** validate `depends_on` (types/contents)
  in `AgentMiddleware.__init__()` so errors point to the middleware that provided
  bad input.'
repository: langchain-ai/langchain
label: Error Handling
language: Python
comments_count: 3
repository_stars: 136312
---

When resolving dependencies or other derived configuration, never “log-and-continue” into an inconsistent internal state.

Apply this standard:
1. **Validate at the source (fail fast):** validate `depends_on` (types/contents) in `AgentMiddleware.__init__()` so errors point to the middleware that provided bad input.
2. **Use narrow exception handling:** during auto-instantiation, catch only expected exception types (e.g., `TypeError`/`ValueError` from constructor/args). Avoid broad `except Exception`.
3. **Preserve invariants:** if auto-instantiation fails, do **not** proceed to dereference structures that assume the dependency exists. Either:
   - raise a clear error immediately, or
   - explicitly check presence before access.
4. **Make errors visible:** use `warning`/`error` (or raise) rather than DEBUG-only logs so failures are actionable in real runs.

Example pattern (inspired by the discussed failure mode):
```python
instance_by_class: dict[type, Middleware] = {}

try:
    instance_by_class[dep_class] = dep_class()  # auto-instantiation
except TypeError as e:  # narrow expected failures
    # Fail fast with context; do not `continue` and later risk KeyError
    raise ValueError(
        f"Failed to auto-instantiate middleware dependency {dep_class.__name__} "
        f"required by {type(instance).__name__}: {e}"
    ) from e

# Safe access: only when guaranteed present
dep_instance = instance_by_class[dep_class]
```

This prevents delayed, confusing errors (like `KeyError`) and ensures failures are reported with precise, fixable context.