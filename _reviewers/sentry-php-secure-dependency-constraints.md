---
title: Secure dependency constraints
description: When specifying dependency version constraints, always include lower
  version bounds that exclude versions with known security vulnerabilities. For dependencies
  used directly in your code (not just transient dependencies), you have a responsibility
  to prevent users from inadvertently installing vulnerable versions, as this makes
  your own package vulnerable.
repository: getsentry/sentry-php
label: Security
language: Json
comments_count: 1
repository_stars: 1873
---

When specifying dependency version constraints, always include lower version bounds that exclude versions with known security vulnerabilities. For dependencies used directly in your code (not just transient dependencies), you have a responsibility to prevent users from inadvertently installing vulnerable versions, as this makes your own package vulnerable.

Example:
```json
"require": {
    "guzzlehttp/psr7": "^1.8.4|^2.1.1",  // Good: specifies minimum versions without vulnerabilities
    // "guzzlehttp/psr7": "^1.0|^2.0",    // Bad: allows versions with known CVEs
}
```

This practice helps protect your users from security issues like CVE-2022-24775 and similar vulnerabilities. Remember that even if users are responsible for their overall dependency management, you are responsible for the security implications of the code you distribute.