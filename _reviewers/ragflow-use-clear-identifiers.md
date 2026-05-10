---
title: Use Clear Identifiers
description: Use semantically meaningful, convention-compliant names everywhere (parameters,
  variables, fields, classes, constants), and avoid ad-hoc renaming/mapping that can
  create ambiguity or incorrect field exposure.
repository: infiniflow/ragflow
label: Naming Conventions
language: Python
comments_count: 6
repository_stars: 80174
---

Use semantically meaningful, convention-compliant names everywhere (parameters, variables, fields, classes, constants), and avoid ad-hoc renaming/mapping that can create ambiguity or incorrect field exposure.

Apply these rules:
- Name parameters by role: prefer `existing_*` / `incoming_*` (or equivalent) over generic names like `metadata, meta`.
- Follow standard casing:
  - variables/functions: `snake_case`
  - classes: `PascalCase` (e.g., `GroqChat`)
  - constants/settings: `UPPER_SNAKE_CASE` (e.g., `REGISTER_ENABLED`)
- Don’t use misleading string operations for identifier suffixes (e.g., prefer `removesuffix('_app')` over trimming characters with `rstrip`).
- Ensure response/request field mappings don’t duplicate or wrongly alias keys; verify one-to-one intended names.
- If you need derived uniqueness (e.g., appending an index), don’t blindly mutate identifiers at the call site—validate the format or normalize earlier so downstream code isn’t surprised.

Example (naming parameters by role):
```python
def update_metadata_to(existing_metadata: dict, incoming_metadata: dict) -> dict:
    """Merge incoming metadata payload into an existing metadata mapping."""
    existing_metadata.update(incoming_metadata)
    return existing_metadata
```