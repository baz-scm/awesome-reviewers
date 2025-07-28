---
title: Explicit error propagation
description: Functions should raise exceptions with meaningful messages instead of
  returning False, None, or silently catching all exceptions. This allows calling
  code to properly understand what went wrong and take appropriate action.
repository: comfyanonymous/ComfyUI
label: Error Handling
language: Python
comments_count: 5
repository_stars: 83726
---

Functions should raise exceptions with meaningful messages instead of returning False, None, or silently catching all exceptions. This allows calling code to properly understand what went wrong and take appropriate action.

**Key principles:**
- Raise specific exceptions instead of returning error indicators like False or None
- Provide descriptive error messages that help diagnose the problem
- Avoid catching and silently swallowing all exceptions unless absolutely necessary
- Ensure calling code can distinguish between success and failure states

**Example of problematic pattern:**
```python
def path_is_low_integrity_writable(path):
    result = subprocess.run([ICACLS_PATH, path], capture_output=True, text=True)
    if result.returncode != 0:
        # Silent failure - calling code doesn't know what went wrong
        return False
    return does_permit_low_integrity_write(result.stdout)
```

**Improved approach:**
```python
def path_is_low_integrity_writable(path):
    result = subprocess.run([ICACLS_PATH, path], capture_output=True, text=True)
    if result.returncode != 0:
        raise PermissionError(f"Failed to check ACL for path {path}: {result.stderr}")
    return does_permit_low_integrity_write(result.stdout)
```

**Additional considerations:**
- Use appropriate exception types (ValueError, FileNotFoundError, etc.) rather than generic Exception
- Document when functions are expected to return ExecutionBlocker vs raise exceptions
- Track both success and failure states explicitly in execution flows
- Add logging for error conditions even when exceptions are raised