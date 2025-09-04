---
title: preserve thread-local state
description: When launching threads in DSPy, ensure that child threads inherit the
  parent thread's local overrides to maintain consistent behavior across concurrent
  executions. DSPy uses thread-local settings that must be properly propagated to
  avoid subtle runtime issues.
repository: stanfordnlp/dspy
label: Concurrency
language: Python
comments_count: 3
repository_stars: 27813
---

When launching threads in DSPy, ensure that child threads inherit the parent thread's local overrides to maintain consistent behavior across concurrent executions. DSPy uses thread-local settings that must be properly propagated to avoid subtle runtime issues.

**Critical Implementation Pattern:**
```python
from dspy.dsp.utils.settings import thread_local_overrides

def _wrap_function(self, function):
    def wrapped(item):
        # Capture parent thread's overrides
        original_overrides = thread_local_overrides.overrides
        # Create isolated copy for this thread
        thread_local_overrides.overrides = thread_local_overrides.overrides.copy()
        try:
            return function(item)
        finally:
            # Restore original state
            thread_local_overrides.overrides = original_overrides
    return wrapped

# When launching threads, pass parent overrides:
parent_overrides = thread_local_overrides.overrides.copy()
executor.submit(cancellable_function, parent_overrides, item)
```

**Why This Matters:**
- DSPy maintains critical settings in thread-local storage that affect model behavior
- Failure to properly handle this "will very subtly ruin strange things"
- Each thread needs an isolated copy of settings while inheriting parent context
- This is essential for consistent behavior in parallel evaluation, bootstrapping, and other concurrent operations

**When to Apply:**
- Any time you use `ThreadPoolExecutor` or similar threading mechanisms
- When implementing parallel execution in DSPy components
- Before refactoring existing single-threaded code to use concurrency

This pattern ensures that DSPy's internal state management works correctly across all concurrent operations, preventing hard-to-debug issues that only manifest under specific threading conditions.