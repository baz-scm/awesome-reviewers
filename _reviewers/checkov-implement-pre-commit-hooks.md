---
title: Implement pre-commit hooks
description: Configure pre-commit hooks to automatically run security and quality
  scanning tools before code is committed to your repository. This creates an early
  feedback loop in the development process, catching issues before they proceed to
  CI/CD pipelines.
repository: bridgecrewio/checkov
label: CI/CD
language: Markdown
comments_count: 2
repository_stars: 7667
---

Configure pre-commit hooks to automatically run security and quality scanning tools before code is committed to your repository. This creates an early feedback loop in the development process, catching issues before they proceed to CI/CD pipelines.

Example implementation for Checkov:
1. Install pre-commit: `pip install pre-commit`
2. Add a `.pre-commit-config.yaml` file to your project:
```yaml
repos:
- repo: https://github.com/bridgecrewio/checkov
  rev: 2.0.399  # specify version here
  hooks:
  - id: checkov
    verbose: true
    args: [--soft-fail]
```
3. Install the hooks: `pre-commit install`

This integration ensures that every commit is automatically scanned for security issues, configuration problems, and compliance violations before it reaches your main codebase or triggers further pipeline steps.