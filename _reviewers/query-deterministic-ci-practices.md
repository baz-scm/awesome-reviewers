---
title: Deterministic CI Practices
description: 'When touching CI/CD workflows, keep execution deterministic and CI stable:


  - **Don’t duplicate steps**: if a publish script already runs tests, avoid running
  `test:ci` again in the workflow.'
repository: tanstack/query
label: CI/CD
language: Yaml
comments_count: 7
repository_stars: 49380
---

When touching CI/CD workflows, keep execution deterministic and CI stable:

- **Don’t duplicate steps**: if a publish script already runs tests, avoid running `test:ci` again in the workflow.
- **Remove redundant conditionals**: if `on:` branch filters already restrict when a workflow/job runs, don’t keep extra `if:` checks that always evaluate the same way.
- **No lockfile churn**: if you didn’t change dependencies, **don’t commit `pnpm-lock.yaml`**. If it changed accidentally (wrong pnpm version, etc.), reset it back to the target branch.
- **Configure required CI secrets**: integrations like Codecov must use GitHub Actions secrets (e.g., `CODECOV_TOKEN`) and supported action versions.
- **Verify vs autofix separation**: “verify-only” checks that detect problems (but don’t automatically fix) belong in CI, while autofix should only handle tasks that can be auto-corrected.

Example (remove redundant `if` when triggers already constrain branches):
```yaml
on:
  push:
    branches: ['main', 'alpha', 'beta', 'rc']

jobs:
  test-and-publish:
    # No extra `if:` needed here; branch filter already limits execution
    runs-on: ubuntu-latest
    steps:
      - run: pnpm run test:pr --parallel=3
```