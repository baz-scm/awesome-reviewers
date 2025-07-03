---
title: Specific exception handling
description: 'Always catch specific exception types rather than using generic `except
  Exception` blocks when you know which exceptions to expect. Using specific exception
  types:'
repository: pytorch/pytorch
label: Error Handling
language: Python
comments_count: 4
repository_stars: 91169
---

Always catch specific exception types rather than using generic `except Exception` blocks when you know which exceptions to expect. Using specific exception types:

1. Improves code clarity by making the expected failure modes explicit
2. Prevents accidentally masking unexpected errors that should be propagated
3. Makes debugging easier by allowing unrelated errors to surface properly

When catching exceptions:

```python
# Bad practice
try:
    value = int(some_float)
except Exception as exc:  # Too broad, catches everything
    handle_error()

# Good practice
try:
    value = int(some_float)
except (ValueError, OverflowError) as exc:  # Specific exceptions
    # Now we handle only the errors we expect
    handle_error()
```

If you're logging errors before re-raising, include both stdout and stderr for better debugging:

```python
try:
    subprocess.run(cmd.split(), capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Command failed:\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}", file=sys.stderr)
    raise  # Re-raise to propagate the error
```

Only catch generic exceptions when you have a compelling reason, such as protecting critical cleanup operations, and even then consider whether specific exception types would be more appropriate.
