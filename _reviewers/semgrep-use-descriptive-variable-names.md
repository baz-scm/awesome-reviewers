---
title: Use descriptive variable names
description: Choose variable and parameter names that clearly communicate their purpose
  and avoid misleading or cryptic naming. Names should be self-documenting and reduce
  cognitive load for other developers.
repository: semgrep/semgrep
label: Naming Conventions
language: Python
comments_count: 3
repository_stars: 12598
---

Choose variable and parameter names that clearly communicate their purpose and avoid misleading or cryptic naming. Names should be self-documenting and reduce cognitive load for other developers.

Key principles:
- Avoid names that don't match their actual purpose (e.g., `ref_if_deployment_name` when it's really about branch availability)
- Prefer descriptive terms over abbreviations (e.g., "selected" and "ignored" instead of "SEL" and "IGN")
- When multiple variables have similar purposes, ensure their relationship is clear through naming

Example of improvement:
```python
# Before: Confusing relationship between parameters
def decide_engine_type(requested_engine, engine_flag):
    requested_engine = engine_flag  # Unclear why both exist

# After: Clear purpose and relationship
def decide_engine_type(engine_flag):
    requested_engine = engine_flag  # Or just use engine_flag directly
```

This reduces confusion during code reviews and makes the codebase more maintainable by ensuring names accurately reflect their semantic meaning.