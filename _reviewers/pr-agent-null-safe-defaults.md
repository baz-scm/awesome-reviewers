---
title: Null-safe Defaults
description: When handling settings, parsed model outputs, and lookup results, assume
  values may be missing (None/empty), omitted, or of the wrong type. Prevent NoneType
  and KeyError crashes by applying a consistent null-safety pattern.
repository: the-pr-agent/pr-agent
label: Null Handling
language: Python
comments_count: 10
repository_stars: 12523
---

When handling settings, parsed model outputs, and lookup results, assume values may be missing (None/empty), omitted, or of the wrong type. Prevent NoneType and KeyError crashes by applying a consistent null-safety pattern.

Standards:
1) Default missing configuration/flags
- Always use safe defaults when reading optional settings values.
- Avoid direct attribute/key access without fallback.

2) Defensive access to dict/list payloads
- Use `.get()` for optional keys.
- Validate required keys before using them; if missing, early-return (or skip the item) with a log.

3) Handle lookup failures explicitly
- If a search can fail (e.g., target file/line not found), check the result and do not proceed.

4) Guard against wrong types / absent fields
- If a value is expected to be a string/number, verify type before doing string ops or comparisons.

5) Avoid mutable default arguments
- Use `None` defaults and create a new list inside the function.

Example pattern:
```python
def publish_inline_comment(payload: dict, settings: dict, diff_files: list):
    # 1) Default optional config
    default_status = settings.get("azure_devops", {}).get("default_comment_status") or "closed"

    # 2) Defensive dict access
    feedback = payload.get("PR Feedback") or {}
    suggestions = feedback.get("Code suggestions") or []

    for s in suggestions:
        # 3) Validate required fields
        relevant_file = (s.get("relevant file") or "").strip()
        relevant_line = (s.get("relevant line in file") or "").strip()
        content = s.get("suggestion content")
        if not relevant_file or not relevant_line or content is None:
            continue

        # 4) Handle lookup failure
        target_file = next((f for f in diff_files if f.filename.strip() == relevant_file), None)
        if target_file is None:
            # skip instead of crashing
            continue

        # proceed safely...
```

6) Tests
- Add/extend unit tests for: missing config keys, None fields, empty payloads, and lookup-not-found scenarios (to ensure these paths return safely instead of throwing).