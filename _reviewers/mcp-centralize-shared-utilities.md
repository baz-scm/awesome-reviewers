---
title: Centralize shared utilities
description: When code has repeated “plumbing” (string templating/formatting, pagination/envelopes,
  client setup, session/ctx extraction, embedding serialization, etc.), move it into
  a shared helper/utility and keep stable imports/constants at module scope. This
  reduces drift, improves readability, and keeps formatting behavior consistent across
  tools.
repository: awslabs/mcp
label: Code Style
language: Python
comments_count: 11
repository_stars: 9545
---

When code has repeated “plumbing” (string templating/formatting, pagination/envelopes, client setup, session/ctx extraction, embedding serialization, etc.), move it into a shared helper/utility and keep stable imports/constants at module scope. This reduces drift, improves readability, and keeps formatting behavior consistent across tools.

Rules:
- Avoid per-call duplication: don’t re-derive the same context/session values or re-import the same modules inside many functions—hoist to module top and/or use a single shared choke point.
- For repeated formatting/envelope logic (pagination metadata, response shaping), centralize it in a shared utility (e.g., `format_response` or a dedicated formatter) instead of re-implementing in each tool.
- For large embedded strings (especially SQL), prefer triple-quoted literals and keep SQL clearly readable.
- If configuration/config-factory logic grows (conditional parsing, routing), extract it from `__init__.py` into a dedicated module (e.g., `factory.py` or `config_builder.py`) for testability and style consistency.

Example (hoist and extract):

```python
# module scope (not inside each function)
import json

from .rum_queries import build_rum_report  # example shared import

async def _run_tool(ctx, action: str, **kwargs):
    # shared choke point / formatter logic here
    report = await build_rum_report(action=action, **kwargs)
    return json.dumps(report, indent=2)

# tool handlers call the shared helper; no repeated imports/formatting
async def errors_tool(app_monitor_name: str, start_time: str, end_time: str) -> str:
    return await _run_tool(None, 'errors', app_monitor_name=app_monitor_name,
                            start_time=start_time, end_time=end_time)
```

Apply this standard during refactors: if you can point to the same pattern being repeated in multiple functions/files (even if “almost the same”), extract it and reuse it everywhere.