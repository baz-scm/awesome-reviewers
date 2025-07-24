---
title: specific defensive error handling
description: Implement specific exception handling and defensive programming practices
  to prevent generic errors from masking real issues and provide graceful degradation
  when operations fail.
repository: docker/compose
label: Error Handling
language: Python
comments_count: 3
repository_stars: 35858
---

Implement specific exception handling and defensive programming practices to prevent generic errors from masking real issues and provide graceful degradation when operations fail.

Key principles:
1. **Catch specific exceptions** rather than generic `Exception` to avoid hiding legitimate errors
2. **Implement defensive checks** before accessing data structures or external resources
3. **Provide sensible defaults** when operations fail to ensure graceful degradation

Example of problematic generic exception handling:
```python
try:
    ctnr.kill()
except Exception:  # Too broad - hides real issues
    pass
```

Better approach with specific exception handling:
```python
try:
    ctnr.kill()
except docker.errors.APIError:  # Specific to expected failure
    log.warning(f"Failed to kill container {ctnr.name}")
```

Example of defensive programming:
```python
# Check before accessing to prevent IndexError
containers = project.up(service_names=[service.name])
matching_containers = [c for c in containers if c.service == service.name]
if not matching_containers:
    raise OperationFailedError("Could not bring up the requested service")
container = matching_containers[0]
```

This approach ensures errors are handled appropriately without masking underlying issues, while providing users with meaningful feedback when operations fail.