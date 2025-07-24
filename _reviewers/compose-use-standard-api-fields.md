---
title: Use standard API fields
description: When designing APIs or interfaces, prioritize using existing standard
  fields and patterns from established APIs rather than creating custom implementations.
  This ensures consistency across tools and reduces cognitive load for users.
repository: docker/compose
label: API
language: Python
comments_count: 4
repository_stars: 35858
---

When designing APIs or interfaces, prioritize using existing standard fields and patterns from established APIs rather than creating custom implementations. This ensures consistency across tools and reduces cognitive load for users.

Key principles:
1. **Leverage existing API responses**: Use fields that are already provided by underlying APIs instead of computing custom values
2. **Align with established tools**: Match parameter ordering, naming conventions, and option sets from widely-used tools in the same domain
3. **Provide complete interfaces**: Include both long and short forms of options, and maintain feature parity with reference implementations

Example from Docker Compose:
```python
# Instead of creating custom status formatting
container.human_readable_state

# Use the standard Status field from Docker API
container.status  # Returns "Up 5 minutes" format used by docker CLI
```

This approach improves user experience through familiarity, reduces maintenance burden by leveraging tested implementations, and ensures compatibility with existing tooling and documentation.