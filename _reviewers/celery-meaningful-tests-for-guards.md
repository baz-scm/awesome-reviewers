---
title: Meaningful Tests For Guards
description: When adding tests for new behavior, deprecations, or environment-dependent
  code paths, ensure the test actually exercises the intended branch (avoid vacuous
  passing) and assert the concrete observable effect.
repository: celery/celery
label: Testing
language: Python
comments_count: 8
repository_stars: 28464
---

When adding tests for new behavior, deprecations, or environment-dependent code paths, ensure the test actually exercises the intended branch (avoid vacuous passing) and assert the concrete observable effect.

Apply this checklist:
1) Force the guard conditions
- If production code checks for installed modules / feature flags / config presence, your test must set up that environment.
- Example pattern for module presence guards:

```python
from unittest.mock import MagicMock, patch

with patch.dict(
    sys.modules,
    {
        'gevent': MagicMock(),
        # add 'eventlet' similarly if needed
    },
    clear=False,
):
    worker.on_start()
    # assert warning/log behavior here
```

2) Test the user-visible outcome (not just “no crash”)
- For deprecations: assert the warning is emitted and the method returns/behaves as expected.
- For behavioral changes: add a targeted unit test for the changed logic and update PR documentation/changelog as requested.

3) Choose the right level to avoid flakiness
- If correctness depends on wall-clock/timezone transitions (DST folds, etc.), prefer deterministic unit tests that control inputs.
- If you must do integration, keep it minimal and prefer existing smoke-test infrastructure over bespoke environment control.

4) Assert precisely
- Tighten assertions to the expected contract (e.g., exact routing key matching) and, for logging, assert on the presence/absence of specific messages.

Following these rules prevents tests that “pass vacuously,” improves regression protection for behavior changes/deprecations, and keeps higher-level tests from becoming brittle.