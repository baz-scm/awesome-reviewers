---
title: Scoped configuration defaults
description: 'When updating `pyproject.toml` (lint/type/dependency config), keep changes
  minimal and future-safe: enable/disable rules deliberately, scope suppressions to
  the smallest scope, avoid broad “select everything” patterns that can introduce
  unintended auto-fixes, remove redundant settings, and bound dependency versions.'
repository: langchain-ai/langchain
label: Configurations
language: Toml
comments_count: 5
repository_stars: 136312
---

When updating `pyproject.toml` (lint/type/dependency config), keep changes minimal and future-safe: enable/disable rules deliberately, scope suppressions to the smallest scope, avoid broad “select everything” patterns that can introduce unintended auto-fixes, remove redundant settings, and bound dependency versions.

Guidelines:
- Prefer targeted suppression over global ignores: use `# noqa: <code>` / `noqa: <rule>` on the specific line; avoid broad `ignorelist` entries unless truly pervasive.
- Don’t enable `select = ["ALL"]` without scoping how fixes are applied. If you must opt into many rules, ensure auto-fixing cannot silently change semantics or readability by pulling in newly-added rules after version bumps.
- Remove redundant mypy/typing flags when the stricter umbrella option already covers them.
- Keep dependency constraints bounded (upper bounds for major versions) so upgrades don’t silently jump compatibility boundaries.

Example (lint config):
```toml
[tool.ruff.lint]
# Prefer explicit lists or ALL only with careful fix scoping.
select = ["ALL"]
# AND ensure you only fix the rules you explicitly trust:
# fixable = ["F", "E", "W"]  # example: opt-in only

[tool.flake8-builtins]
# Prefer per-line suppression over global ignores:
# "id" should usually be handled with:  some_var = id(...)  # noqa: A002
ignorelist = []
```

Example (mypy config):
```toml
[tool.mypy]
strict = true
# Avoid redundant flags like strict_bytes if strict already implies it.
# strict_bytes = true  # remove
```

Example (dependency bounds):
```toml
dependencies = [
  "langgraph>=0.6.0,<1.0.0",
]
```