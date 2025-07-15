---
title: Proactive dependency security
description: Always maintain dependencies at their latest secure versions, even when
  automated vulnerability scanning tools (like `npm audit`) don't report issues. Regularly
  check release notes and security advisories for your dependencies, as some security
  fixes may not be detected by automated tools.
repository: nestjs/nest
label: Security
language: Json
comments_count: 1
repository_stars: 71767
---

Always maintain dependencies at their latest secure versions, even when automated vulnerability scanning tools (like `npm audit`) don't report issues. Regularly check release notes and security advisories for your dependencies, as some security fixes may not be detected by automated tools.

When a team member identifies a security vulnerability:
1. Verify the vulnerability exists
2. Upgrade to the fixed version promptly
3. Document the change

Example:
```json
// Update vulnerable dependencies immediately when discovered
{
  "dependencies": {
    "@fastify/middie": "8.3.3",  // Updated from 8.3.1 which had security issues
    // Other dependencies...
  }
}
```

Consider implementing a regular dependency review process, occurring at least monthly, to proactively identify and address security vulnerabilities.