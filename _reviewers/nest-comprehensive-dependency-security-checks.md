---
title: Comprehensive dependency security checks
description: Regularly check dependencies for security vulnerabilities using multiple
  sources, not just npm audit. As shown in the discussion, some vulnerabilities may
  not be reported by npm audit but are still present and documented elsewhere.
repository: nestjs/nest
label: Security
language: Json
comments_count: 1
repository_stars: 71766
---

Regularly check dependencies for security vulnerabilities using multiple sources, not just npm audit. As shown in the discussion, some vulnerabilities may not be reported by npm audit but are still present and documented elsewhere.

When a security vulnerability is identified:
1. Promptly update the affected dependency to a patched version
2. Consult release notes to verify the fix
3. Document the update reason in commit messages

Example:
```json
// Before - vulnerable dependency
{
  "dependencies": {
    "@fastify/middie": "8.3.1"  // Has security vulnerability
  }
}

// After - updated dependency
{
  "dependencies": {
    "@fastify/middie": "8.3.3"  // Security vulnerability fixed
  }
}
```

Consider implementing automated tools or scheduled workflows to periodically check for dependency vulnerabilities beyond what npm audit reports.