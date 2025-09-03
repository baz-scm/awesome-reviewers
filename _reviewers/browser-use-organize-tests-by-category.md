---
title: organize tests by category
description: Structure test suites into clear, logical categories and run them as
  separate CI jobs for better parallelization, maintainability, and failure identification.
  This approach makes it easier to understand test failures, enables targeted testing,
  and improves CI performance through parallel execution.
repository: browser-use/browser-use
label: Testing
language: Yaml
comments_count: 2
repository_stars: 69139
---

Structure test suites into clear, logical categories and run them as separate CI jobs for better parallelization, maintainability, and failure identification. This approach makes it easier to understand test failures, enables targeted testing, and improves CI performance through parallel execution.

Organize tests by functional area or technology stack, such as:
- Browser-related tests (different browser engines, CDP integration)
- Model/API tests (different AI providers)  
- Functionality tests (UI interactions, features)

Example CI matrix configuration:
```yaml
strategy:
  matrix:
    test:
      - browser/patchright
      - browser/user_binary
      - browser/remote_cdp
      - models/openai
      - models/google
      - models/anthropic
      # TODO: keep adding more in the future
      # - models/azure
      # - models/deepseek
      # - functionality/click
      # - functionality/tabs
```

This structure allows teams to easily add new test categories, run specific test subsets, and quickly identify which area of the codebase has issues when tests fail.