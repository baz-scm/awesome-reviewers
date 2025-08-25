---
title: enforce consistent SSO flows
description: When single sign-on (SSO) is enabled as the primary authentication mechanism,
  ensure all authentication entry points consistently redirect to the SSO endpoint
  without complex conditional logic. Avoid respecting secondary authentication parameters
  that could create inconsistent behavior or potential security gaps.
repository: discourse/discourse
label: Security
language: JavaScript
comments_count: 1
repository_stars: 44898
---

When single sign-on (SSO) is enabled as the primary authentication mechanism, ensure all authentication entry points consistently redirect to the SSO endpoint without complex conditional logic. Avoid respecting secondary authentication parameters that could create inconsistent behavior or potential security gaps.

Complex conditionals around authentication flows can introduce vulnerabilities where users might bypass the intended SSO flow or encounter inconsistent authentication behavior across different routes.

Example of problematic code:
```javascript
// Avoid complex conditionals when SSO is primary auth
if (auth_immediately && enable_discourse_connect) {
  // Only redirect in some cases
  window.location = getURL(`/session/sso?return_path=${returnPath}`);
}
```

Preferred approach:
```javascript
// When SSO is enabled, always redirect regardless of other flags
if (enable_discourse_connect) {
  const returnPath = cookie("destination_url") 
    ? getURL("/") 
    : encodeURIComponent(url);
  window.location = getURL(`/session/sso?return_path=${returnPath}`);
}
```

This ensures that SSO remains the authoritative authentication method when enabled, preventing potential bypass scenarios and maintaining consistent security posture across all authentication flows.