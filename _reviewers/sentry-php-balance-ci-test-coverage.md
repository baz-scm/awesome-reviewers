---
title: Balance CI test coverage
description: 'Configure CI workflows to optimize both comprehensive testing and resource
  usage. For resource-intensive tests that may cause issues (like OOM errors with
  code coverage), split test suites and run coverage selectively:'
repository: getsentry/sentry-php
label: CI/CD
language: Yaml
comments_count: 4
repository_stars: 1873
---

Configure CI workflows to optimize both comprehensive testing and resource usage. For resource-intensive tests that may cause issues (like OOM errors with code coverage), split test suites and run coverage selectively:

```yaml
# Example: Split test suites for better resource management
- name: Run unit tests with coverage
  run: vendor/bin/phpunit --testsuite unit --coverage-clover=coverage.xml
- name: Run resource-intensive tests without coverage
  run: vendor/bin/phpunit --testsuite intensive --no-coverage
```

Include quick tests (like benchmarks under a few seconds) in regular CI runs to prevent code rot, but consider separate workflows for longer-running tests. Use CI platform features like `skip_branch_with_pr: true` to prevent duplicate builds when PRs are open, optimizing overall CI resource usage.