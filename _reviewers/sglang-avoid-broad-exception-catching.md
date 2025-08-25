---
title: Avoid broad exception catching
description: Avoid using overly broad exception handling like `except Exception` as
  it can mask specific errors and make debugging difficult. Instead, catch specific
  exception types when possible, or convert generic exceptions to more informative,
  specific error types with meaningful messages.
repository: sgl-project/sglang
label: Error Handling
language: Python
comments_count: 2
repository_stars: 17245
---

Avoid using overly broad exception handling like `except Exception` as it can mask specific errors and make debugging difficult. Instead, catch specific exception types when possible, or convert generic exceptions to more informative, specific error types with meaningful messages.

When you must catch broad exceptions, immediately convert them to specific error types that provide context about what went wrong and why. This helps with debugging and prevents silent failures.

Example of problematic broad catching:
```python
try:
    speculative_algo = global_server_args_dict.get("speculative_algorithm", None)
    if speculative_algo is not None and hasattr(speculative_algo, "is_eagle"):
        return speculative_algo.is_eagle()
except Exception:  # Too broad - what could fail here?
    return False
```

Better approach with specific error handling:
```python
try:
    ip_str, port_str = distributed_init_method.split(":")[-2:]
    ip = ip_str.split("/")[-1]
    port = int(port_str)
except (ValueError, IndexError) as e:  # Specific exceptions
    raise RuntimeError(
        f"Cannot parse host and port from {distributed_init_method}: {str(e)}"
    )
```

This approach makes errors more actionable for developers and prevents masking of unexpected issues that should be addressed.