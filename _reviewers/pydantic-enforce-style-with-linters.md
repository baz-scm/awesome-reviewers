---
title: Enforce style with linters
description: Use automated linting tools to enforce consistent code style across the
  project, but be deliberate about which rules to include or exclude. When adding
  new linters or rules, evaluate their impact on the codebase before fully adopting
  them.
repository: pydantic/pydantic
label: Code Style
language: Toml
comments_count: 2
repository_stars: 24377
---

Use automated linting tools to enforce consistent code style across the project, but be deliberate about which rules to include or exclude. When adding new linters or rules, evaluate their impact on the codebase before fully adopting them.

For configuration files like pyproject.toml:
```toml
[tool.ruff]
select = [
    'D1',     # pydocstyle
    'PIE',    # flake8-pie
]
# Ignore rules with explicit reasoning
ignore = ['D105', 'D107', 'PIE804']  # Document exceptions with comments
```

When making style-related changes, prefer solutions that can be automatically enforced rather than relying on manual review. Consider adding appropriate pre-commit hooks for consistent formatting. If a tool would generate too many changes at once (like the discussed toml-fmt), consider gradual adoption or documenting the manual style requirements clearly.