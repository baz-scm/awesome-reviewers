---
title: Logging consistency and safety
description: 'When writing/adjusting code, treat logging as part of error handling:


  - Use the right level: log request- or operation-failure conditions at `error`/`exception`
  (not `warning`).'
repository: the-pr-agent/pr-agent
label: Logging
language: Python
comments_count: 7
repository_stars: 12523
---

When writing/adjusting code, treat logging as part of error handling:

- Use the right level: log request- or operation-failure conditions at `error`/`exception` (not `warning`).
- In `except` blocks, prefer `get_logger().exception(...)` (or `error(...)`) and include identifying context (IDs, URLs, comment_id, PR/issue number) so logs are traceable.
- Use structured/context fields (e.g., `artifact={...}`) rather than passing arbitrary objects (like dicts) as separate arguments to the logger—this can cause formatting/type issues.
- Avoid `print` statements for debug; use `get_logger().debug(...)` with the same context.
- Don’t comment out logging used for exception diagnostics—either log it or remove the dead code.

Example pattern:
```python
try:
    ...
except Exception as e:
    get_logger().exception(
        "Failed to publish inline code comments fallback",
        artifact={
            "comment_id": comment_id,
            "error": repr(e),
            "pr_number": pr_number,
        },
    )
    raise
```
For non-exception unexpected formats:
```python
get_logger().warning(
    "Unexpected response format",
    artifact={"response": str(response_tuple)},
)
```