---
title: Stable CI Workflow Policy
description: 'When modifying CI workflows, keep pipelines deterministic, resource-efficient,
  and transparent:


  - **Gate expensive jobs:** Run integration (and other heavyweight suites) only after
  unit tests succeed to save resources. Use job dependencies (e.g., `needs: unit-tests`).'
repository: celery/celery
label: CI/CD
language: Yaml
comments_count: 4
repository_stars: 28464
---

When modifying CI workflows, keep pipelines deterministic, resource-efficient, and transparent:

- **Gate expensive jobs:** Run integration (and other heavyweight suites) only after unit tests succeed to save resources. Use job dependencies (e.g., `needs: unit-tests`).
- **Make test setup deterministic:** Enforce test discovery/layout rules so contributors can’t accidentally introduce conflicting setup files (e.g., alternative `conftest.py`) via unexpected directory nesting. Fail fast with clear error messages.
- **Be explicit about CI matrix coverage:** Any test exclusions (Python versions, test tiers) must be justified by stability/maintainability constraints and should include a plan to revisit once flakiness is fixed.

Example pattern (job gating):
```yaml
jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest -m unit

  integration-tests:
    needs: unit-tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest -m integration
```

Example pattern (deterministic discovery):
```bash
nested=$(find t/integration -mindepth 2 -name 'test_*.py')
if [ -n "$nested" ]; then
  echo "::error::Integration test files must live at t/integration/ root, not in subdirectories: $nested"
  exit 1
fi
```