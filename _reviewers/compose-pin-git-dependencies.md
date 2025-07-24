---
title: Pin git dependencies
description: When using git references for dependencies in configuration files like
  requirements.txt, always pin to specific commit SHAs instead of branch names to
  ensure reproducible builds and prevent unexpected changes from being automatically
  pulled in.
repository: docker/compose
label: Configurations
language: Txt
comments_count: 2
repository_stars: 35858
---

When using git references for dependencies in configuration files like requirements.txt, always pin to specific commit SHAs instead of branch names to ensure reproducible builds and prevent unexpected changes from being automatically pulled in.

Using branch names like `master` or `main` can lead to non-deterministic builds where different developers or deployment environments might pull different versions of the code, potentially introducing breaking changes or inconsistent behavior.

Example of what to avoid:
```
git+https://github.com/docker/docker-py.git@master#egg=docker-py
```

Example of proper pinning:
```
git+https://github.com/docker/docker-py.git@a1b2c3d4e5f6789012345678901234567890abcd#egg=docker-py
```

This practice ensures that all team members and deployment environments use exactly the same version of the dependency, making builds more predictable and debugging easier when issues arise.