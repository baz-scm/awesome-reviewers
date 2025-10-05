---
title: Initialize and validate values
description: 'Always initialize variables with sensible default values and validate
  inputs to prevent null reference errors and undefined behavior. This includes three
  key practices:'
repository: commaai/openpilot
label: Null Handling
language: Python
comments_count: 4
repository_stars: 58214
---

Always initialize variables with sensible default values and validate inputs to prevent null reference errors and undefined behavior. This includes three key practices:

1. **Initialize with defaults**: Set initial values in constructors to avoid uninitialized state issues, especially when methods may be called before updates occur.

2. **Validate inputs**: Check that input parameters meet expected formats and constraints before processing, even if you don't validate the full domain.

3. **Handle missing values**: Provide explicit fallback behavior when parameters or configuration values might be missing or deleted.

Example from the codebase:
```python
# Good: Initialize with default value
def __init__(self):
    self.avg_dt = MovingAverage(100)
    self.avg_dt.add_value(self._interval)  # Prevents uninitialized state

# Good: Validate input format
def setEsimProfile(iccid: str):
    # Validate input is valid ICCID format
    if not is_valid_iccid(iccid):
        raise ValueError("Invalid ICCID format")
    HARDWARE.get_sim_lpa().switch_profile(iccid)

# Good: Handle missing parameters with fallback
def read_param(self):
    param_value = self.params.get('LongitudinalPersonality')
    if param_value is not None:
        self.personality = param_value
    else:
        self.personality = log.LongitudinalPersonality.standard  # Fallback
```

This prevents runtime errors from null references, uninitialized variables, and invalid inputs while ensuring predictable behavior.