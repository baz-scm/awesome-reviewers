---
title: Validate access controls
description: Always implement comprehensive validation for access control mechanisms
  to prevent unauthorized access and privilege escalation. This includes validating
  user permissions, enforcing tenant isolation, and preventing bypass through direct
  API calls.
repository: langgenius/dify
label: Security
language: Python
comments_count: 4
repository_stars: 114231
---

Always implement comprehensive validation for access control mechanisms to prevent unauthorized access and privilege escalation. This includes validating user permissions, enforcing tenant isolation, and preventing bypass through direct API calls.

Key validation points:
1. **Tenant isolation**: Validate tenant_id early in methods to prevent cross-tenant access
2. **Input validation**: Add validation for user inputs that could bypass restrictions (e.g., email uniqueness checks)
3. **Privilege escalation prevention**: When handling IDs from untrusted sources, always include tenant context
4. **Proper HTTP responses**: Return 403 for authorization failures, not 404

Example implementation:
```python
def get_execution_by_id(self, execution_id: str, tenant_id: Optional[str] = None):
    # When tenant_id is None, it's the caller's responsibility to ensure proper data isolation
    # If execution_id comes from untrusted sources (e.g., API request), 
    # set tenant_id to prevent horizontal privilege escalation
    if tenant_id is None:
        # Log warning or require tenant_id for security
        pass
    
    # Early tenant validation
    if dataset.tenant_id != user.current_tenant_id:
        raise NoPermissionError("Access denied")
    
    # Additional permission validation
    if not self._has_permission(user, execution_id):
        abort(403)  # Not 404 - proper HTTP semantics
```

This approach ensures that security boundaries are maintained at multiple layers and prevents common authorization vulnerabilities.