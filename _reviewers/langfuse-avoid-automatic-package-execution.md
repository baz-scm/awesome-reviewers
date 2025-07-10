---
title: Avoid automatic package execution
description: Using `npx --yes` bypasses security prompts and automatically installs
  packages without verification, which could lead to supply chain attacks if package
  names are typosquatted or compromised. Always install required tools as explicit
  dependencies in your project.
repository: langfuse/langfuse
label: Security
language: Shell
comments_count: 1
repository_stars: 13574
---

Using `npx --yes` bypasses security prompts and automatically installs packages without verification, which could lead to supply chain attacks if package names are typosquatted or compromised. Always install required tools as explicit dependencies in your project.

**Instead of this (risky):**
```bash
npx --yes @datadog/datadog-ci sourcemaps upload "$DIST_PATH"
```

**Do this instead (safer):**
```bash
# In package.json, add as a dev dependency:
# "@datadog/datadog-ci": "^x.y.z"

# Then in your script:
npx @datadog/datadog-ci sourcemaps upload "$DIST_PATH"
```

By explicitly declaring dependencies, you ensure consistent versions, improve security posture, and enable your team to review all dependencies during security audits.