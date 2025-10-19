---
name: handle-exceptions-with-specificity
description: Use specific exception types and avoid masking errors through overly
  broad exception handling or default values. This improves error diagnosis and system
  reliability.
version: '1.0'
---
# Handle exceptions with specificity

Use specific exception types and avoid masking errors through overly broad exception handling or default values. This improves error diagnosis and system reliability.

Key guidelines:
1. Use concrete exception types instead of catching broad Exception classes
2. Don't provide default values that could mask errors
3. Don't swallow exceptions without proper handling
4. Create custom exceptions for domain-specific errors

Example - Instead of:
```python
try:
    result = client.refresh_token(token)
except Exception as e:
    log.error("Error refreshing token: %s", e)
    return None
```

Use:
```python
def refresh_token(self, refresh_token: str) -> str:
    """Refresh the access token for the user."""
    client = self._get_keycloak_client()
    tokens = client.refresh_token(refresh_token)
    log.info("Token refreshed successfully")
    return tokens["access_token"]
```

This approach:
- Makes error scenarios explicit and traceable
- Prevents masking of underlying issues
- Improves system observability
- Enables proper error handling at appropriate levels
