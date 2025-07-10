---
title: Document CI pipeline comprehensively
description: 'Ensure CI/CD pipeline documentation accurately reflects the complete
  workflow, including job dependencies, execution order, and all operations performed
  by each step. When documenting CI processes:'
repository: Homebrew/brew
label: CI/CD
language: Markdown
comments_count: 3
repository_stars: 44168
---

Ensure CI/CD pipeline documentation accurately reflects the complete workflow, including job dependencies, execution order, and all operations performed by each step. When documenting CI processes:

1. List CI jobs in their logical execution order, with dependency relationships clearly indicated
2. Document all operations performed by each job, not just the primary ones
3. Specify clear conditions for when different CI-related tools should be used

For example, when documenting a test job that runs multiple commands:

```markdown
## CI Jobs

- `CI / syntax`: This is run first to check whether the PR passes `brew style` and `brew typecheck`. If this job fails, the following jobs will not run.
- `CI / test everything (macOS)`: This runs multiple tests including:
  - `brew tests`
  - `brew update-tests`
  - `brew readall`
  - `brew test-bot --only-formulae --test-default-formula`
  - `brew doctor`
```

Complete documentation helps maintainers understand the full CI pipeline, troubleshoot failures effectively, and follow consistent processes when merging changes.