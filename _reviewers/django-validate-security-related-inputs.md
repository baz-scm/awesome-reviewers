---
title: Validate security-related inputs
description: Always validate and sanitize all inputs that influence security-related
  functionality at the application level, rather than relying on underlying systems
  to handle invalid inputs. This prevents potential security vulnerabilities and provides
  clearer error messages to developers.
repository: django/django
label: Security
language: Python
comments_count: 3
repository_stars: 84182
---

Always validate and sanitize all inputs that influence security-related functionality at the application level, rather than relying on underlying systems to handle invalid inputs. This prevents potential security vulnerabilities and provides clearer error messages to developers.

When implementing security features:

1. Sanitize user inputs before using them in security contexts
2. Validate configuration values against expected types and ranges
3. Provide informative error messages that aid debugging without exposing sensitive details

**Example 1:** Sanitizing search inputs to prevent injection
```python
def psql_escape(query: str):
    """Replace unsafe chars with space and convert multiple spaces to single."""
    return normalize_spaces(_spec_chars_re.sub(" ", query))
```

**Example 2:** Validating security configuration values
```python
def validate_csp_setting(name, value):
    if value is not None and not isinstance(value, dict):
        raise ValueError(
            f"The Content Security Policy setting '{name}' must be a dictionary (got {value!r} instead)."
        )
```

**Example 3:** Validating security-critical parameters
```python
def set_weight(self, weight):
    if weight is not None and weight.upper() not in ('A', 'B', 'C', 'D'):
        raise ValueError(f"Weight must be one of A, B, C, or D (got {weight!r} instead).")
    self.weight = weight
```

Always perform input validation as early as possible in your code, before the values are used in any security-critical operations. This prevents security vulnerabilities and provides better developer experience with meaningful errors.