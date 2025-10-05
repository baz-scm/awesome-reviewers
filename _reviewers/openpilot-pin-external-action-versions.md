---
title: pin external action versions
description: Always pin external GitHub Actions to specific commit hashes rather than
  using tags or branch names, and prefer built-in runner capabilities when available.
  This improves security by preventing supply chain attacks and ensures reproducible
  builds.
repository: commaai/openpilot
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 58214
---

Always pin external GitHub Actions to specific commit hashes rather than using tags or branch names, and prefer built-in runner capabilities when available. This improves security by preventing supply chain attacks and ensures reproducible builds.

Unpinned actions create security vulnerabilities and can break workflows when external maintainers update their actions. Additionally, using built-in runner features reduces external dependencies and improves performance.

Example of proper pinning:
```yaml
# Bad - using tag
- uses: stefanzweifel/git-auto-commit-action@v5

# Good - pinned to commit hash  
- uses: stefanzweifel/git-auto-commit-action@8621497c8c39c72f3e2a999a13b1c01d91af5b75

# Even better - use built-in capabilities when possible
# Instead of actions/setup-python@v5.3.0, use:
runs-on: ubuntu-24.04  # comes with python 3.12 pre-installed
```

Always research if the runner already provides the needed functionality before adding external dependencies.