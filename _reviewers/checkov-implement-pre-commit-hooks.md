---
title: Implement pre-commit hooks
description: Automate quality and security checks by implementing pre-commit hooks
  in your Git repositories to catch issues early in the development process. Pre-commit
  hooks run specified checks automatically when files change, before code is committed,
  helping to enforce standards without manual intervention.
repository: bridgecrewio/checkov
label: CI/CD
language: Markdown
comments_count: 2
repository_stars: 7668
---

Automate quality and security checks by implementing pre-commit hooks in your Git repositories to catch issues early in the development process. Pre-commit hooks run specified checks automatically when files change, before code is committed, helping to enforce standards without manual intervention.

To set up pre-commit hooks:

1. Install the pre-commit framework: https://pre-commit.com/#install
2. Create a `.pre-commit-config.yaml` file in your repository root with configurations for tools like Checkov:

```yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/bridgecrewio/checkov.git
    rev: 2.0.556  # Use the latest version
    hooks:
    -   id: checkov
        args: [--quiet]
```

3. Install the hooks with `pre-commit install`

This practice improves CI/CD pipelines by shifting quality control left, reducing failed builds, and allowing developers to fix issues before they enter the main pipeline. Configure hooks for linting, security scanning, formatting, and other quality checks relevant to your project.