---
title: Null and Empty Handling
description: 'Apply a consistent null/empty handling pattern for configuration and
  user-provided values:


  - Treat “present but empty” inputs (e.g., env vars set to `""`) as invalid rather
  than silently falling back. Prefer behavior that surfaces a clear configuration
  error.'
repository: TauricResearch/TradingAgents
label: Null Handling
language: Python
comments_count: 3
repository_stars: 71953
---

Apply a consistent null/empty handling pattern for configuration and user-provided values:

- Treat “present but empty” inputs (e.g., env vars set to `""`) as invalid rather than silently falling back. Prefer behavior that surfaces a clear configuration error.
- Guard nullable/optional values before use (including `None` from prompt/selection flows). Fail gracefully and consistently.
- Normalize user input (e.g., `strip()`), validate required fields, and handle the empty/None case explicitly.
- Add tests for failure paths (null/empty inputs) to prevent regressions.

Example pattern:
```python
import os

# 1) Empty env values should not silently fall back
base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
# If base_url is "", downstream will raise a clear configuration error.

# 2) Guard nullable/custom inputs
value = prompt_fn()  # may return None or ""
if value is None:
    # graceful exit / clear error
    raise ValueError("Missing model name")
model = value.strip()
if not model:
    raise ValueError("Please enter a model name.")

# 3) In tests, assert error behavior for None/empty cases
```

This prevents “quiet localhost” (or other misleading defaults) and ensures null/empty misconfigurations are visible, handled safely, and protected by test coverage.