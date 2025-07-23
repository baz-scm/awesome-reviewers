---
title: Update security patches regularly
description: Always keep dependencies, runtime environments, and libraries updated
  with the latest security patches to mitigate known vulnerabilities. Prioritize security
  updates even for minor version changes.
repository: microsoft/vscode
label: Security
language: Other
comments_count: 1
repository_stars: 174887
---

Always keep dependencies, runtime environments, and libraries updated with the latest security patches to mitigate known vulnerabilities. Prioritize security updates even for minor version changes.

Example:
```
# Incorrect
# .nvmrc
22.15.1

# Correct
# .nvmrc
22.17.1  # Latest version with security fixes
```

Regular dependency updates are a critical security practice. When security patches are available (like Node.js 22.17.1 that fixes security issues), they should be applied promptly rather than waiting for future update cycles. Establish a process for monitoring security advisories related to your project dependencies and implement patches in a timely manner.