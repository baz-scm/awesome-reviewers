---
title: Document parameter choices
description: 'Always add explanatory comments for parameters or configuration options
  that aren''t self-explanatory from their names or context. These comments should
  explain:'
repository: neondatabase/neon
label: Documentation
language: Python
comments_count: 2
repository_stars: 19015
---

Always add explanatory comments for parameters or configuration options that aren't self-explanatory from their names or context. These comments should explain:

1. What the parameter does
2. Why a specific value was chosen
3. What different values would mean (especially in tests with multiple modes)

This helps future developers understand your reasoning and the implications of parameter choices.

Examples:

```python
# Good - explains why retry_on_failures is needed
env.storage_controller.reconcile_until_idle(timeout_secs=60, retry_on_failures=True)  # retry_on_failures needed because reconciliation may encounter transient errors during split operations

# Good - explains test parameters
@pytest.mark.parametrize("with_compute_ctl", [False, True], ids=["standard", "compute-ctl"])
# with_compute_ctl: Tests prewarm behavior both with and without compute controller integration
def test_lfc_prewarm(neon_simple_env: NeonEnv, with_compute_ctl: bool):
    ...
```

Especially important for:
- Boolean flags (the reason for enabling/disabling)
- Magic numbers (why this specific value)
- Test parameters (what aspect each parameter tests)
- Configuration options with non-default values