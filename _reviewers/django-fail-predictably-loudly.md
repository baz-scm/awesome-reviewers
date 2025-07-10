---
title: Fail predictably, loudly
description: Design APIs that fail explicitly and predictably when used incorrectly.
  When an operation is attempted in an inappropriate state, raise a specific exception
  rather than returning None or an unexpected value. This helps developers catch misuse
  early rather than encountering subtle bugs later.
repository: django/django
label: API
language: Txt
comments_count: 3
repository_stars: 84182
---

Design APIs that fail explicitly and predictably when used incorrectly. When an operation is attempted in an inappropriate state, raise a specific exception rather than returning None or an unexpected value. This helps developers catch misuse early rather than encountering subtle bugs later.

For example, when accessing result properties that are only valid in certain states:

```python
def get_exception(self):
    if self.status != ResultStatus.FAILED:
        raise ValueError("Exception is only available when task has FAILED status")
    return self._exception

def get_return_value(self):
    if self.status != ResultStatus.COMPLETE:
        raise ValueError("Return value is only available when task has COMPLETE status")
    return self._return_value
```

Similarly, be cautious with timing-sensitive operations. When an API accepts relative time values (like timedeltas), document clearly when these values are resolved to absolute times, as this can lead to surprising behavior.

When modifying existing APIs, prioritize maintaining consistent behavior. If changing return types is necessary, ensure the new types support all previously documented behavior or provide clear migration paths. Sudden changes in return values or behavior create confusion and lead to bugs that are difficult to diagnose.