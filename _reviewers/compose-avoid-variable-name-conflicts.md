---
title: Avoid variable name conflicts
description: Choose variable names that prevent conflicts with system variables, external
  tools, and variables in overlapping scopes. Use prefixes or distinct naming to differentiate
  purpose and avoid unintended overrides.
repository: docker/compose
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 35858
---

Choose variable names that prevent conflicts with system variables, external tools, and variables in overlapping scopes. Use prefixes or distinct naming to differentiate purpose and avoid unintended overrides.

For system/tool conflicts, use prefixed names:
```makefile
# Instead of LDFLAGS (conflicts with rpm/deb packaging)
GO_LDFLAGS ?= -s -w -X ${PKG}/internal.Version=${VERSION}
```

For same-scope conflicts, use different names for different purposes:
```dockerfile
# Instead of same name for ARG and ENV
ARG GIT_COMMIT=unknown
ENV DOCKER_COMPOSE_GITSHA=$GIT_COMMIT
```

This prevents situations where variables are unexpectedly overridden by external tools or conflicting declarations in the same context.