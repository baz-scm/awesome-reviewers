---
title: Code Style, Typing, DRY
description: 'Adopt a “type-safe, clean, DRY” style for readability and maintainability.


  - Prefer module-scope imports: don’t re-import a module inside a function if it
  already exists at file scope.'
repository: openai/openai-python
label: Code Style
language: Python
comments_count: 9
repository_stars: 30731
---

Adopt a “type-safe, clean, DRY” style for readability and maintainability.

- Prefer module-scope imports: don’t re-import a module inside a function if it already exists at file scope.
- Keep type annotations precise:
  - Annotate intermediate locals when introducing them (e.g., `schema_param: ResponseFormatParam = {...}`).
  - Use accurate container types (e.g., `Dict[str, str]` for headers) rather than `Any`.
  - Avoid `# type: ignore` when the mismatch can be fixed by correcting the related type(s).
  - For version-specific utilities, structure branches so type checkers can understand both paths without extra ignores.
  - When typing wrappers that forward args/kwargs, use `ParamSpec` to preserve call signatures.
- Reduce duplication/readability issues:
  - Factor repeated parsing/processing into a small helper used by both sync and async variants.
  - When code organization is getting messy due to shared logic, prefer private methods on the owning class over adding more items to generic utility modules (when circular imports allow).
- Remove dead/unused code: don’t introduce variables (like a spinner cycle) that aren’t used.

Example (import + typed local + helper pattern):
```py
# module scope
import json


def parse_stream_line(line: bytes) -> str:
    if not line or line == b"data: [DONE]":
        return ""
    if hasattr(line, "decode"):
        line = line.decode("utf-8")
    if line.startswith("data: "):
        line = line[len("data: "):]
    return line


def parse_stream(rbody):
    for line in rbody:
        out = parse_stream_line(line)
        if out:
            yield out


def some_function() -> "ResponseFormatParam":
    schema_param: "ResponseFormatParam" = {"type": "text"}
    return schema_param
```

Applying these consistently will improve clarity (fewer surprises), maintainability (less duplication), and type-checker effectiveness (fewer ignores and safer refactors).