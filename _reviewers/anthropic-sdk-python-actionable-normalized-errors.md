---
title: Actionable normalized errors
description: 'When adding error handling for failure scenarios (infinite/looping behavior,
  retries, or other unbounded processes), ensure two things:


  1) Normalize/validate error-relevant inputs before they affect control flow.'
repository: anthropics/anthropic-sdk-python
label: Error Handling
language: Python
comments_count: 2
repository_stars: 3392
---

When adding error handling for failure scenarios (infinite/looping behavior, retries, or other unbounded processes), ensure two things:

1) Normalize/validate error-relevant inputs before they affect control flow.
- Edge values (e.g., `math.inf`) must be converted to safe integer bounds before using constructs like `range()`.

2) Make raised exceptions actionable.
- If the failure is usually triggered by configuration (e.g., an overly small threshold), include a message that tells the user what to change.

Example pattern:
```python
import math
import sys

def retry_loop(max_retries):
    if max_retries is math.inf or max_retries >= sys.maxsize:
        range_limit = sys.maxsize
    else:
        range_limit = int(max_retries) + 1

    for _ in range(range_limit):
        yield


def detect_potentially_infinite_compaction(threshold):
    # ... if two consecutive compactions happen:
    raise RuntimeError(
        "Potentially infinite compaction detected. "
        f"Increase the compaction threshold (current: {threshold}) to avoid two consecutive compaction iterations."
    )
```
Apply this standard so exceptions don’t just fail— they guide the fix and avoid additional crashes caused by invalid/edge inputs.