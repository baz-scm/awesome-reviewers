---
title: maintain clean CI configuration
description: Keep CI/CD configuration files clean and self-documenting by removing
  outdated comments, using descriptive parameter names, and avoiding redundant specifications.
  Remove TODO comments that no longer reflect the current state of the codebase, choose
  parameter names that clearly indicate their scope and purpose, and rely on existing
  configuration files (like...
repository: prisma/prisma
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 42967
---

Keep CI/CD configuration files clean and self-documenting by removing outdated comments, using descriptive parameter names, and avoiding redundant specifications. Remove TODO comments that no longer reflect the current state of the codebase, choose parameter names that clearly indicate their scope and purpose, and rely on existing configuration files (like package.json) rather than duplicating version specifications.

Example of good practices:
```yaml
# Remove outdated comments
flavor: ['js_pg', 'js_libsql', 'js_d1', 'js_better_sqlite3']

# Use descriptive parameter names
driverAdapterTestJobTimeout:  # clearly indicates job-level timeout

# Avoid redundant version specs when package.json handles it
- name: Setup PNPM
  uses: pnpm/action-setup@v4
  # No version specified - uses packageManager from package.json
```

This approach reduces maintenance overhead, prevents confusion from stale documentation, and makes CI configurations more reliable and easier to understand.