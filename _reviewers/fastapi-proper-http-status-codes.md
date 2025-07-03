---
title: Proper HTTP status codes
description: When implementing authentication and authorization systems, use semantically
  correct HTTP status codes to accurately convey the nature of security-related failures.
  This improves API security by providing accurate information to clients without
  exposing unnecessary details.
repository: fastapi/fastapi
label: Security
language: Python
comments_count: 4
repository_stars: 86871
---

When implementing authentication and authorization systems, use semantically correct HTTP status codes to accurately convey the nature of security-related failures. This improves API security by providing accurate information to clients without exposing unnecessary details.

Specifically:
- Use 403 Forbidden when a user is authenticated but lacks authorization (e.g., inactive user, insufficient permissions)
- Use 401 Unauthorized for authentication failures (invalid or missing credentials)
- Use 400 Bad Request only for malformed client requests

Example implementation:
```python
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    return current_user
```

This approach follows REST principles and improves security by providing consistent and accurate status codes that properly communicate authorization states without revealing implementation details.