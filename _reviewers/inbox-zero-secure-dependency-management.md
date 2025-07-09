---
title: Secure dependency management
description: 'Always maintain secure dependencies by following these two critical
  security practices:


  1. **Keep dependencies updated with the latest security patches** - Regularly check
  for and apply updates that contain security fixes. Pin to specific versions but
  review them frequently.'
repository: elie222/inbox-zero
label: Security
language: Json
comments_count: 1
repository_stars: 8267
---

Always maintain secure dependencies by following these two critical security practices:

1. **Keep dependencies updated with the latest security patches** - Regularly check for and apply updates that contain security fixes. Pin to specific versions but review them frequently.

2. **Always maintain a lockfile for security auditing** - Ensure your project has a lockfile (package-lock.json, yarn.lock, etc.) to enable proper vulnerability scanning.

Example implementation:
```json
{
  "scripts": {
    "start": "node build/index.js",
    "build": "tsc && node -e \"require('fs').chmodSync('build/index.js', '755')\"",
    "audit": "npm audit",
    "update-check": "npm outdated"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "1.6.1",  // Updated to latest version with security patches
    "zod": "3.24.2"
  }
}
```

To validate dependencies:
1. Run `npm i --package-lock-only` to generate/update the lockfile
2. Execute `npm audit` to check for known vulnerabilities
3. Use `npm outdated` to identify packages with available updates