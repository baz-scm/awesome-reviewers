---
title: Safe async-to-sync bridging
description: 'When code must run async coroutines from a synchronous context (or vice
  versa), be deliberate about correctness, extensibility, and dependency handling:'
repository: pallets/flask
label: Concurrency
language: Python
comments_count: 4
repository_stars: 75022
---

When code must run async coroutines from a synchronous context (or vice versa), be deliberate about correctness, extensibility, and dependency handling:

1. Detect coroutine functions robustly. Don't just check the raw callable — unwrap bound methods and `functools.partial` wrappers before testing, since `inspect.iscoroutinefunction` can give false negatives otherwise:
```python
def iscoroutinefunction(func):
    while inspect.ismethod(func):
        func = func.__func__
    while isinstance(func, functools.partial):
        func = func.func
    return inspect.iscoroutinefunction(func)
```
Prefer using the standard library's version when available instead of reintroducing a compatibility shim.

2. Make the actual async-to-sync execution step an overridable hook (e.g. a dedicated `async_to_sync` method) rather than baking the conversion logic into a larger dispatch method. This lets users swap in alternate event-loop/runner implementations without duplicating the coroutine-detection boilerplate.

3. Treat the async runtime bridge (e.g. `asgiref`) as an optional dependency. Import it lazily inside the function that needs it and raise a clear, actionable error if it's missing, rather than requiring it unconditionally:
```python
try:
    import asgiref
except ImportError:
    raise RuntimeError("Install asgiref in order to run async views.")
```

4. Guard against shared mutable state when the same options/config object may be reused across multiple registrations or calls (e.g. blueprint options dicts). Copy before mutating so that one registration/call doesn't leak state into another:
```python
for blueprint, bp_options in self._blueprints:
    bp_options = bp_options.copy()  # avoid mutating shared state
```

Applying these practices keeps async/sync bridges correct across wrapped callables, extensible for custom runners, dependency-light for users who don't need async, and free of subtle bugs caused by shared mutable state across repeated registrations or invocations.</description>
</invoke>
