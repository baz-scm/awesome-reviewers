---
title: Prevent unintended CI behaviors
description: Ensure CI/CD pipelines maintain predictable and reliable behavior by
  avoiding changes that introduce unexpected side effects or alter default behaviors.
  This includes preventing automatic actions like image pushing when not explicitly
  requested, using consistent tooling approaches across similar operations, and properly
  handling unreliable components.
repository: docker/compose
label: CI/CD
language: Go
comments_count: 4
repository_stars: 35858
---

Ensure CI/CD pipelines maintain predictable and reliable behavior by avoiding changes that introduce unexpected side effects or alter default behaviors. This includes preventing automatic actions like image pushing when not explicitly requested, using consistent tooling approaches across similar operations, and properly handling unreliable components.

Key practices:
- Preserve default behaviors unless explicitly overridden by user intent
- Use consistent tooling approaches (e.g., if using vendored clients for standard builds, use them for related operations too)
- Skip or isolate flaky tests in CI environments rather than letting them destabilize the pipeline
- Add comprehensive verification to ensure expected behaviors
