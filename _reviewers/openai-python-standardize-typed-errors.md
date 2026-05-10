---
title: Standardize Typed Errors
description: Use consistent, typed exceptions at the point of failure, with structured
  context, and never rely on unchecked/bypassed paths that convert errors into later
  crashes.
repository: openai/openai-python
label: Error Handling
language: Python
comments_count: 9
repository_stars: 30731
---

Use consistent, typed exceptions at the point of failure, with structured context, and never rely on unchecked/bypassed paths that convert errors into later crashes.

Apply:
- Credential/auth failures: raise your library’s canonical error (e.g., `OpenAIError`) for all credential/installation/mode-resolution issues; wrap underlying exceptions via `raise ... from exc`.
- Parsing/validation failures: when decoding/validating responses, catch schema/JSON errors and raise a dedicated typed error (e.g., `ContentFormatError`) that includes actionable context (such as `raw_content`).
- Polling/loops: always enforce timeouts/terminal-state handling; if the loop ends due to timeout or failure, raise a clear exception immediately (avoid letting later code assume fields exist).
- Exception chaining: prefer `raise NewError(...) from exc` and don’t manually set `__cause__`.

Example (parsing boundary):
```python
try:
    model_parse_json(MyModel, content)  # or TypeAdapter(...).validate_json
except (pydantic.ValidationError, json.JSONDecodeError) as exc:
    raise ContentFormatError(raw_content=content, error=exc) from exc
```

Example (polling boundary):
```python
start = time.time()
while not until(response):
    if time.time() - start > TIMEOUT_SECS:
        raise OpenAIError("Polling timed out")
    response = self.request(...)[0]
```

This reduces mystery failures (like `KeyError`) and makes errors actionable for users and tests.