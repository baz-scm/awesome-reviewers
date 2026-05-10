---
title: Avoid stray commas
description: When running linters/formatters in CI or scripts, keep command arguments
  syntactically precise and standardized—remove any stray or meaningless punctuation
  (like a standalone comma) and normalize whitespace so commands are unambiguous.
repository: TheAlgorithms/Python
label: Code Style
language: Yaml
comments_count: 2
repository_stars: 220912
---

When running linters/formatters in CI or scripts, keep command arguments syntactically precise and standardized—remove any stray or meaningless punctuation (like a standalone comma) and normalize whitespace so commands are unambiguous.

Also, standardize on the team’s chosen linter (e.g., use Ruff instead of Flake8 when Ruff is the agreed replacement) to keep behavior consistent across environments.

Example (CI lint step):
```yaml
- name: Lint code
  run: |
    uv run ruff check --output-format=github
```
Avoid patterns like:
```yaml
run: uv run ruff check , --output-format=github
```