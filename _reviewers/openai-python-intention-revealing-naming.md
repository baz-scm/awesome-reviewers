---
title: Intention-Revealing Naming
description: 'Write names that clearly communicate meaning, scope/intent, and project
  terminology—especially on public APIs/CLI and when calling helpers.


  Apply:

  - Match canonical terms: use the team/docs/external-provider wording for user-facing
  strings and public parameters (e.g., `endpoint`).'
repository: openai/openai-python
label: Naming Conventions
language: Python
comments_count: 7
repository_stars: 30731
---

Write names that clearly communicate meaning, scope/intent, and project terminology—especially on public APIs/CLI and when calling helpers.

Apply:
- Match canonical terms: use the team/docs/external-provider wording for user-facing strings and public parameters (e.g., `endpoint`).
- Prefer explicit keywords in calls unless arguments are truly positional-only: 
  - Prefer `func(..., api_type=api_type, api_version=api_version)` over relying on position.
- Use underscore markers to signal intent:
  - Use a single leading underscore (`_name`) for “internal/private by convention”.
  - Avoid double-underscore (`__name`) unless you specifically need name-mangling semantics.
  - Prefix intentionally-unused values/fixtures with `_` to satisfy linters and show intent (e.g., `_logger_with_filter`).
- Avoid generic/ambiguous identifiers for integrations: choose distinct module/class names for integrations (e.g., `wandb_logger` / `WandbLogger`) rather than something indistinguishable from general logging.

Example:
```py
api_type, api_version = cls._get_api_type_and_version(api_type, api_version)
url = cls._get_url("edits", None, api_type=api_type, api_version=api_version)

def _check_polling_response(...):
    ...  # internal by convention
```