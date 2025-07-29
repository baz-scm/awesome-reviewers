---
title: avoid redundant tool configuration
description: When configuring code style tools, avoid enabling rules or settings that
  duplicate functionality already provided by other tools in your toolchain. This
  reduces configuration complexity, prevents conflicting rules, and improves maintainability.
repository: python-poetry/poetry
label: Code Style
language: Toml
comments_count: 3
repository_stars: 33496
---

When configuring code style tools, avoid enabling rules or settings that duplicate functionality already provided by other tools in your toolchain. This reduces configuration complexity, prevents conflicting rules, and improves maintainability.

Before adding a new linting rule or formatter setting, verify that it doesn't overlap with existing tools:
- Don't enable `flake8-annotations` (ANN) when using mypy in strict mode
- Don't enable `flake8-quotes` (Q) when using black for formatting  
- Don't specify configuration values that match the tool's defaults

Example from pyproject.toml:
```toml
[tool.ruff]
extend-select = [
    "B",  # flake8-bugbear
    # "ANN",  # flake8-annotations - redundant with mypy strict mode
    "C4",  # flake8-comprehensions
    # "Q",  # flake8-quotes - black handles quote formatting
]

[tool.ruff.isort]
# section-order = [...] # unnecessary, matches default order
```

This approach ensures your style enforcement is consistent, avoids tool conflicts, and keeps configuration files focused on meaningful customizations rather than redundant specifications.