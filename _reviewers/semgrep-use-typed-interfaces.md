---
title: Use typed interfaces
description: Prefer typed interfaces over dictionary access to enable static type
  checking and prevent null reference errors. When accessing data structures, use
  typed objects with defined fields rather than dictionary key access, as this allows
  mypy to detect typos and missing fields at compile time.
repository: semgrep/semgrep
label: Null Handling
language: Python
comments_count: 3
repository_stars: 12598
---

Prefer typed interfaces over dictionary access to enable static type checking and prevent null reference errors. When accessing data structures, use typed objects with defined fields rather than dictionary key access, as this allows mypy to detect typos and missing fields at compile time.

This practice is especially important for optional and nullable fields, where dictionary access can lead to KeyError exceptions or unexpected None values that aren't caught until runtime.

Example:
```python
# Avoid: Dictionary access that mypy cannot validate
show_dataflow_traces = extra["dataflow_traces"]  # Prone to typos, no null safety

# Prefer: Typed interface access
show_dataflow_traces = cli_output_extra.dataflow_traces  # Mypy validates field exists

# For optional fields, be explicit about the type
repo_display_name: str | None = self.repo_display_name  # Clear nullable intent
```

When designing APIs, clearly define whether fields are required or optional (`str | None`) rather than relying on fallback logic, as this makes null handling explicit and prevents unexpected runtime behavior.