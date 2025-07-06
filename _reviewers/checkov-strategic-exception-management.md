---
title: Strategic exception management
description: Choose the appropriate error handling strategy based on the context and
  severity of potential failures. Use exceptions for truly exceptional conditions
  that represent invalid states or unrecoverable errors, while providing graceful
  fallbacks for non-critical failures.
repository: bridgecrewio/checkov
label: Error Handling
language: Python
comments_count: 5
repository_stars: 7668
---

Choose the appropriate error handling strategy based on the context and severity of potential failures. Use exceptions for truly exceptional conditions that represent invalid states or unrecoverable errors, while providing graceful fallbacks for non-critical failures.

**When to fail fast (raise exceptions):**
- When encountering invalid program states that could lead to data corruption or incorrect behavior
- For authentication or authorization failures that shouldn't proceed (e.g., 401/403 responses)
- When detecting conflicting configuration that represents a programming error

```python
# Good: Raising exceptions for invalid program states
def get_record_file_line_range(package: dict[str, Any], file_line_range: list[int] | None) -> list[int]:
    package_line_range = get_package_lines(package)
    if package_line_range and file_line_range:
        raise Exception('Both \'package_line_range\' and \'file_line_range\' are not None. Conflict.')
    # Continue processing with valid state
```

**When to degrade gracefully:**
- For recoverable errors where alternative paths exist
- When user experience would benefit from continued operation
- For non-critical features where failure doesn't compromise core functionality

```python
# Good: Providing graceful fallback for non-critical failures
def get_sso_prismacloud_url(self, report_url: str) -> str:
    # If authentication fails, return the regular URL instead of raising an exception
    request = self.http.request("GET", url_saml_config, headers=headers, timeout=10)
    if request.status >= 300:  # Any error response
        return report_url  # Fallback to standard URL
```

**Best practices:**
1. Use specific exception types rather than generic ones (e.g., `except ValueError:` instead of `except Exception:`)
2. Add validation before operations that might throw exceptions
3. Provide informative error messages that help diagnose the root cause
4. Consider the impact on the user experience when choosing your error handling strategy