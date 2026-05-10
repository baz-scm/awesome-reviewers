---
title: Test isolation and tiers
description: When adding or changing behavior, require unit tests that are (a) comprehensive
  for the logic contract, (b) correctly prioritized/selected via pytest markers, and
  (c) isolated from global state to avoid cross-suite flakiness.
repository: infiniflow/ragflow
label: Testing
language: Python
comments_count: 7
repository_stars: 80174
---

When adding or changing behavior, require unit tests that are (a) comprehensive for the logic contract, (b) correctly prioritized/selected via pytest markers, and (c) isolated from global state to avoid cross-suite flakiness.

Apply it like this:
- Cover the real decision points and fallbacks: defaults, manual-vs-auto modes, empty inputs, type/probe fallbacks, and output shape/values.
- Use the right pytest marker level so the test actually runs in your expected pipeline (e.g., don’t leave important coverage at `p3` if it won’t execute by default). Ensure markers are registered in `pyproject.toml`.
- If tests stub imports or mutate `sys.modules`/env, isolate that mutation with `autouse` fixtures that restore the original state after each test.

Example pattern for isolating `sys.modules` stubs:
```python
import sys
import pytest
from types import ModuleType

@pytest.fixture(autouse=True)
def isolate_sys_modules():
    original = sys.modules.copy()
    try:
        yield
    finally:
        sys.modules.clear()
        sys.modules.update(original)

def test_something_with_stubbed_google_lib():
    sys.modules["googleapiclient"] = ModuleType("googleapiclient")
    # ... import/use code under test safely ...
```

Additionally, for refactors that change call paths, either rely on the expanded unit tests above or attach lightweight scenario-based verification to show behavior is unchanged.