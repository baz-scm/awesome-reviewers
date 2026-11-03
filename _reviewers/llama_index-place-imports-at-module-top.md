---
title: Place imports at module top
description: Keep imports at the top of the file instead of scattering them inside
  `__init__` or method bodies. Lazy, function-local imports (often wrapped in `try/except
  ImportError`) should only be used for genuinely optional dependencies that are not
  required by the package. If a package is already listed as a required dependency
  in `pyproject.toml`, assume it's...
repository: run-llama/llama_index
label: Code Style
language: Python
comments_count: 10
repository_stars: 52785
---

Keep imports at the top of the file instead of scattering them inside `__init__` or method bodies. Lazy, function-local imports (often wrapped in `try/except ImportError`) should only be used for genuinely optional dependencies that are not required by the package. If a package is already listed as a required dependency in `pyproject.toml`, assume it's installed whenever the integration itself is installed — there's no need to guard the import with a try/except, and re-importing it on every method call adds needless overhead. This also applies to standard-library modules (e.g. `io`), which can never fail to import and should never be guarded.

Example of what to avoid:
```python
class CambToolSpec(BaseToolSpec):
    def __init__(self, api_key: Optional[str] = None) -> None:
        from camb.client import CambAI  # required dependency, unnecessarily lazy

        try:
            ...
        except ImportError as exc:
            raise ImportError("camb is required...") from exc
```

Preferred:
```python
from camb.client import CambAI  # top-level, since camb is a required dependency

class CambToolSpec(BaseToolSpec):
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.client = CambAI(api_key=api_key)
```

Reserve lazy imports (with a helpful `ImportError` message) strictly for optional extras that a user may choose not to install.