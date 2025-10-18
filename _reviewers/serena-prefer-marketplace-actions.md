---
title: prefer marketplace actions
description: Before implementing custom tool installation steps in GitHub Actions
  workflows, check if there's an existing setup action available on the GitHub Actions
  marketplace. Marketplace actions are typically more reliable, better maintained,
  and reduce workflow complexity compared to custom installation scripts.
repository: oraios/serena
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 14465
---

Before implementing custom tool installation steps in GitHub Actions workflows, check if there's an existing setup action available on the GitHub Actions marketplace. Marketplace actions are typically more reliable, better maintained, and reduce workflow complexity compared to custom installation scripts.

When adding tool installation to your workflow, first search the marketplace for actions like `setup-<tool>` (e.g., setup-node, setup-python, setup-go). Only implement custom installation logic when no suitable marketplace action exists or when the existing action doesn't meet your specific requirements.

Example of preferred approach:
```yaml
# Preferred: Use marketplace action
- uses: actions/setup-node@v3
  with:
    node-version: '18'

# Avoid when marketplace alternative exists:
- name: Install Node.js manually
  run: |
    curl -fsSL https://nodejs.org/dist/v18.17.0/node-v18.17.0-linux-x64.tar.xz
    # ... custom installation steps
```

This approach reduces maintenance burden, improves reliability, and leverages community-tested solutions.