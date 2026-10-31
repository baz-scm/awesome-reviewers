---
title: Lazy-load expensive imports
description: Avoid paying for expensive work until it is actually needed. Heavy third-party
  dependencies (e.g. `litellm`, `mcp`) must not be imported at module load time if
  importing them triggers significant latency or side effects (network calls, large
  model-cost map fetches, etc.). Instead, move the import into the function or method
  that uses it, and cache the bound...
repository: kyegomez/swarms#pi240310
label: Performance Optimization
language: Python
comments_count: 12
repository_stars: 7337
---

Avoid paying for expensive work until it is actually needed. Heavy third-party dependencies (e.g. `litellm`, `mcp`) must not be imported at module load time if importing them triggers significant latency or side effects (network calls, large model-cost map fetches, etc.). Instead, move the import into the function or method that uses it, and cache the bound symbol in a module-level variable guarded by a `None` check so the import only happens once and existing call sites/tests that patch the module attribute keep working:

```python
completion = None

def _bind_litellm() -> None:
    """Import litellm on first use, not at module import time."""
    global completion
    if completion is None:
        from litellm import completion as _completion
        completion = _completion
```

For type-only usages, prefer `TYPE_CHECKING` guards so static typing still works without forcing a runtime import.

The same principle applies to any computation that is only relevant under a specific condition: compute it inside the guard that actually needs it, rather than unconditionally on every iteration (e.g., only scan a layer for "clean" status when checkpointing is enabled, instead of doing it on every layer regardless). Always validate the impact with a measurement (e.g., import timing before/after) so the optimization is verifiable rather than assumed.