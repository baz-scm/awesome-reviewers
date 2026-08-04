---
title: Consistent Configuration Wiring
description: 'Configuration must be internally consistent: what you declare in `pyproject.toml`
  and document (e.g., env vars) must match what the code actually does, and dependency/tooling
  choices must align with the project’s toolchain.'
repository: awslabs/mcp
label: Configurations
language: Toml
comments_count: 2
repository_stars: 9545
---

Configuration must be internally consistent: what you declare in `pyproject.toml` and document (e.g., env vars) must match what the code actually does, and dependency/tooling choices must align with the project’s toolchain.

Apply this checklist:
- Use realistic, compatible dependency minimums: avoid overly-loose floors that allow ancient API-incompatible releases; avoid version specs with no stable releases.
- Keep tooling dependencies aligned with the chosen workflow (e.g., don’t keep `virtualenv` if you use `uv`).
- If you advertise an environment variable (like `FASTMCP_LOG_LEVEL`), ensure code/config actually reads it and applies it (e.g., configure Loguru at startup).

Example (dependency + logging wiring):
```toml
# pyproject.toml
[project]
dependencies = [
  "fastmcp>=2.13.1", # avoid dangerously loose floors
  # ...
]
# If using uv, avoid redundant virtualenv tooling dependencies.
```
```python
# server.py (startup)
import os
import sys
from loguru import logger

level = os.getenv("FASTMCP_LOG_LEVEL", "INFO")
logger.remove()
logger.add(sys.stderr, level=level)
```

Net effect: fewer “works in README but not in runtime” surprises and fewer dependency-resolution failures caused by inconsistent configuration.