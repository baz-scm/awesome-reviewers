---
title: Proper configuration placement
description: Place configuration files and settings at the appropriate level in your
  repository structure. In monorepos, some configurations must be at the root level
  while others belong at the package level.
repository: langfuse/langfuse
label: Configurations
language: Json
comments_count: 2
repository_stars: 13574
---

Place configuration files and settings at the appropriate level in your repository structure. In monorepos, some configurations must be at the root level while others belong at the package level.

Key guidelines:
- Dependency patches should be configured at the root level of the repository
- Include ephemeral files (like test result artifacts) in `.gitignore` to prevent accidental commits
- Understand which configurations are shared across packages (root) versus package-specific

Example from a monorepo structure:
```json
// Root package.json - for patches and shared overrides
{
  "resolutions": {
    "overrides": {
      "jsonpath-plus": "10.0.7",
      "katex": "^0.16.21",
      "openid-client": "5.6.5"
    },
    "patchedDependencies": {
      "next-auth@4.24.11": "patches/next-auth@4.24.11.patch",
      "openid-client@5.6.5": "patches/openid-client@5.6.5.patch"
    }
  }
}

// .gitignore - exclude ephemeral files
web/test-results/.last-run.json
```

Inappropriate placement of configuration can cause functionality issues or repository pollution.