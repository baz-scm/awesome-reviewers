---
title: Justify CI resource additions
description: Before adding new resources (Dockerfiles, jobs, images) to CI/CD pipelines,
  provide clear justification for their necessity and document how they will be maintained.
  Consider whether the resource will actually run in your CI environment, if existing
  resources could be reused, and who will maintain version updates. For example, instead
  of creating a new...
repository: vitessio/vitess
label: CI/CD
language: Other
comments_count: 2
repository_stars: 19815
---

Before adding new resources (Dockerfiles, jobs, images) to CI/CD pipelines, provide clear justification for their necessity and document how they will be maintained. Consider whether the resource will actually run in your CI environment, if existing resources could be reused, and who will maintain version updates. For example, instead of creating a new Dockerfile for a specific test:

```
# Before: Creating a new Dockerfile that may not be necessary
FROM golang:1.24.3
# ... rest of specialized Dockerfile that might be redundant

# After: Use existing Docker images when possible, or clearly document the need
# for specialized images in CI documentation and CHANGELOG.md
```

Document additions in appropriate CHANGELOG files and consider potential maintenance overhead before expanding CI infrastructure.