---
title: Semantic naming for schemas
description: Use names that communicate intent and framework semantics—especially
  for (a) schemas and (b) callback parameters whose names are used for injection/dispatch.
repository: langchain-ai/langchain
label: Naming Conventions
language: Python
comments_count: 8
repository_stars: 136312
---

Use names that communicate intent and framework semantics—especially for (a) schemas and (b) callback parameters whose names are used for injection/dispatch.

Standards:
- Schema field names must reflect meaning (e.g., distinguish input vs output in attribute naming; if a value is injected at invocation time, name it as such).
- For functions wrapped by decorators/frameworks, use the exact parameter names required by the framework (e.g., `state`, `runtime`, `request`) rather than relying on positional arguments or renaming.
- If a parameter is intentionally unused, rename it with an underscore prefix (e.g., `_self`, `_runtime`) instead of adding suppression comments.
- For behavior-bearing identifiers, include the salient behavior in the name or docstring (e.g., if a regex compilation depends on a specific flag like `MULTILINE`, the name should not hide that nuance).
- For metadata keys used for precedence/selection, keep naming consistent and self-explanatory (the key name should tell you what it identifies and where it comes from).

Example (callback arg naming + unused naming):
```python
from typing import Any
from langgraph.types import interrupt

def before_agent(state: Any, runtime: Any) -> dict[str, Any]:
    # framework-injected names: keep as-is
    return {"ok": True, "state": state, "runtime": runtime}

def before_agent_unused(runtime: Any, state: Any) -> dict[str, Any]:
    # if intentionally unused, use underscore prefix
    _ = state
    return {"ok": True}

async def headless_coroutine(_config: Any, **kwargs: Any) -> Any:
    # intentionally unused config -> underscore
    return interrupt({"args": kwargs})
```

Applying this will reduce confusion in schema-driven tooling, prevent subtle runtime bugs caused by incorrect parameter names, and make behavior easier to understand during review.