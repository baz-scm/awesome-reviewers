---
title: Simple explicit interfaces
description: Design API interfaces to be simple and explicit rather than hiding complexity
  behind elaborate fallbacks or conditional logic. When core functionality is unavailable,
  fail explicitly with clear error messages instead of implementing complex workarounds.
  Push complexity and decision-making to the caller rather than embedding it within
  the API implementation.
repository: oraios/serena
label: API
language: Python
comments_count: 3
repository_stars: 14465
---

Design API interfaces to be simple and explicit rather than hiding complexity behind elaborate fallbacks or conditional logic. When core functionality is unavailable, fail explicitly with clear error messages instead of implementing complex workarounds. Push complexity and decision-making to the caller rather than embedding it within the API implementation.

Key principles:
- Fail fast and explicitly when required functionality is unsupported
- Use direct assertions instead of conditional checks that mask expectations
- Keep interface signatures simple and delegate complex logic to callers
- Handle type inconsistencies explicitly rather than silently converting

Example of preferred approach:
```python
# Good: Simple interface, explicit failure
def rename_symbol(self, file_path: str, line: int, column: int, new_name: str) -> WorkspaceEdit | None:
    if not self.server.supports_rename():
        raise UnsupportedOperationError("Language server does not support rename operations")
    return self.server.send.rename(params)

# Good: Explicit assertions instead of conditionals
allow_symbol = next((s for s in symbol_list if s.get("name") == "allow"), None)
assert allow_symbol is not None, "allow symbol should always be found"

# Good: Simple interface pushes list creation to caller
def _run_command(command: list[str], logger: LanguageServerLogger, cwd: str) -> None:
    # Caller is responsible for creating the command list
```

This approach makes APIs more predictable, easier to test, and clearer about their expectations and limitations.