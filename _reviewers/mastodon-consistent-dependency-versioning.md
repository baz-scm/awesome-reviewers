---
title: consistent dependency versioning
description: Maintain consistent version constraint patterns across all dependencies
  in configuration files and avoid unstable versions that can cause build issues.
  Use caret (^) constraints uniformly for predictable updates within compatible ranges,
  and employ resolutions when necessary to prevent automatic resolution to beta or
  unstable versions.
repository: mastodon/mastodon
label: Configurations
language: Json
comments_count: 2
repository_stars: 48691
---

Maintain consistent version constraint patterns across all dependencies in configuration files and avoid unstable versions that can cause build issues. Use caret (^) constraints uniformly for predictable updates within compatible ranges, and employ resolutions when necessary to prevent automatic resolution to beta or unstable versions.

When package managers resolve to unstable versions, use explicit resolutions to enforce stable versions:

```json
{
  "devDependencies": {
    "@vitest/browser": "^3.2.1",
    "@vitest/coverage-v8": "^3.2.0",
    "@vitest/ui": "^3.2.1"
  },
  "resolutions": {
    "vite": "^6.3.5"
  }
}
```

This prevents issues like TypeScript compatibility problems from beta releases while maintaining consistent constraint patterns. Remember to remove forced resolutions once stable versions become available.