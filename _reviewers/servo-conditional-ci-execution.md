---
title: conditional CI execution
description: Use appropriate conditional statements in CI workflows to ensure steps
  execute under the right circumstances and handle different environments gracefully.
repository: servo/servo
label: CI/CD
language: Yaml
comments_count: 5
repository_stars: 32962
---

Use appropriate conditional statements in CI workflows to ensure steps execute under the right circumstances and handle different environments gracefully.

Key practices:
- Use `if: ${{ always() }}` for cleanup/finalization steps that must run regardless of previous step failures
- Use environment-specific conditions like `if: ${{ runner.environment != 'self-hosted' }}` for steps that should only run on certain runner types
- Implement fallback strategies when preferred infrastructure (like self-hosted runners) is unavailable
- Ensure required workflow parameters are provided across all entrypoints when adding new required inputs

Example from the discussions:
```yaml
- name: Publish artifact marking this job as done
  uses: actions/upload-artifact@v4
  if: ${{ always() }}  # Ensures cleanup runs even if job fails
  with:
    # artifact configuration

- name: Setup Python
  if: ${{ runner.environment != 'self-hosted' }}  # Only on GitHub-hosted
  uses: ./.github/actions/setup-python

- name: Change Mirror Priorities  
  if: ${{ runner.environment != 'self-hosted' }}  # Skip on self-hosted
  uses: ./.github/actions/apt-mirrors
```

This approach prevents workflow failures due to missing infrastructure, ensures proper cleanup, and optimizes resource usage by skipping unnecessary steps on different runner types.