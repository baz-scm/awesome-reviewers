---
title: optimize workflow maintainability
description: Design CI/CD workflows for long-term maintainability by using consolidated
  commands and extracting reusable components. Instead of listing individual build
  steps that may change over time, prefer consolidated npm scripts like `npm run pretest`
  that encapsulate the full build process. This approach reduces the need to update
  workflows when underlying build...
repository: cline/cline
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 48299
---

Design CI/CD workflows for long-term maintainability by using consolidated commands and extracting reusable components. Instead of listing individual build steps that may change over time, prefer consolidated npm scripts like `npm run pretest` that encapsulate the full build process. This approach reduces the need to update workflows when underlying build requirements change. For complex inline logic, extract functionality into custom GitHub Actions rather than embedding lengthy scripts directly in workflow files.

Example of maintainable approach:
```yaml
# Preferred: Uses consolidated command
- name: Build Tests and Extension  
  run: npm run pretest

# Instead of: Individual commands that require updates
- name: Check Types
  run: npm run check-types
- name: Lint
  run: npm run lint  
- name: Build Extension
  run: npm run compile
```

For reusable logic, create custom actions instead of inline scripts to improve readability and enable reuse across workflows.