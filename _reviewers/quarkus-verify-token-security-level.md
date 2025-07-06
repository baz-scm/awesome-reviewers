---
title: Verify token security level
description: When refreshing or updating authentication tokens, always verify the
  new token maintains or exceeds the original token's security level. This applies
  to WebSocket connections, step-up authentication scenarios, or any case where tokens
  are refreshed during an active session.
repository: quarkusio/quarkus
label: Security
language: Other
comments_count: 9
repository_stars: 14667
---

When refreshing or updating authentication tokens, always verify the new token maintains or exceeds the original token's security level. This applies to WebSocket connections, step-up authentication scenarios, or any case where tokens are refreshed during an active session.

For security integrity, implement these essential checks:

1. Verify principal identity remains consistent (same user)
2. Confirm required roles and permissions are preserved
3. Validate that Authentication Context Class Reference (ACR) values meet or exceed requirements

```java
// Example for WebSocket token refresh
@OnTextMessage
String processMessage(RequestDto request) {
    // 1. Verify same principal/subject
    if (!securityIdentity.getPrincipal().getName().equals(newTokenPrincipal)) {
        throw new SecurityException("Principal mismatch during token refresh");
    }
    
    // 2. Re-apply security checks with new token
    if (!hasRequiredRoles(newToken, originalRequiredRoles)) {
        throw new SecurityException("Insufficient privileges in new token");
    }
    
    // 3. Check ACR values for step-up authentication
    if (requiredAcr != null && !newToken.getClaim("acr").contains(requiredAcr)) {
        throw new SecurityException("Required authentication level not met");
    }
    
    // Update token only after all checks pass
    webSocketSecurity.updateSecurityIdentity(newToken);
}
```

Failing to verify these security properties when refreshing tokens could allow privilege escalation or unauthorized access if a compromised or less-privileged token replaces a more secure one.