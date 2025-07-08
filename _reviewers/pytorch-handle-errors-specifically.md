---
title: Handle errors specifically
description: Always be explicit and specific when handling errors rather than using
  catch-all approaches or implicit conventions. This improves code robustness, debuggability,
  and maintainability.
repository: pytorch/pytorch
label: Error Handling
language: Python
comments_count: 5
repository_stars: 91345
---

Always be explicit and specific when handling errors rather than using catch-all approaches or implicit conventions. This improves code robustness, debuggability, and maintainability.

When catching exceptions:
1. Catch specific exception types instead of using broad exception handlers
2. Only catch exceptions you can meaningfully handle
3. Consider returning None for recoverable failures instead of catching arbitrary exceptions

```python
# Don't do this - catching all exceptions masks problems
try:
    result = complex_operation()
except Exception as exc:
    result = default_value  # Which errors should actually be handled this way?

# Do this - be specific about what you're catching
try:
    result = complex_operation()
except MemoryError:
    # Handle specific memory issues
    raise RuntimeError("Insufficient memory for operation") from exc
except KeyError as e:
    # Handle missing keys appropriately
    return None  # Indicate failure with explicit return
```

When raising or signaling errors:
1. Raise specific exceptions with clear messages rather than returning special values
2. Use enums or dedicated types for error conditions instead of magic numbers
3. Place validation before state mutation to keep system consistent during exceptions

```python
# Don't do this - using special return values is error-prone
def check_if_supported():
    if not meets_requirements():
        return False  # Caller might miss this!
    # ...

# Do this - be explicit about errors
def check_if_supported():
    if not meets_requirements():
        raise RuntimeError("Requirements not met: missing XYZ")
    # ...
    
# Order operations to maintain system integrity
def perform_mutation(self, key):
    # First validate - may raise exceptions
    if key not in self.valid_keys:
        raise_args_mismatch()
    
    # Only mutate state after validation passes
    self.should_reconstruct = True
    self.output.side_effects.mutation(self)
```

By being specific about errors, you make code easier to debug and maintain while preventing your system from entering invalid states.