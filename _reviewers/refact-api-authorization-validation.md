---
title: API authorization validation
description: All API endpoints must implement proper authorization checks before processing
  requests, especially when authentication mechanisms like tokens are available. When
  adding new API routes, verify that appropriate authorization validation is in place
  to prevent unauthorized access to sensitive functionality.
repository: smallcloudai/refact
label: Security
language: Python
comments_count: 1
repository_stars: 3114
---

All API endpoints must implement proper authorization checks before processing requests, especially when authentication mechanisms like tokens are available. When adding new API routes, verify that appropriate authorization validation is in place to prevent unauthorized access to sensitive functionality.

Example implementation pattern:
```python
async def _rh_stats(self, account: str = "user"):
    # Add authorization check before processing
    if not self._validate_admin_token():
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if not self._stats_service.is_ready:
        # ... rest of endpoint logic
```

Reference existing authorization patterns in your codebase (such as CompletionsRouter) to ensure consistency in how authorization is implemented across different endpoints. This prevents security vulnerabilities where sensitive data or operations could be accessed without proper authentication.