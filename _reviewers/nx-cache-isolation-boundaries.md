---
title: cache isolation boundaries
description: When documenting caching systems, clearly specify cache isolation boundaries
  and access scopes to prevent confusion about cache behavior. Distinguish between
  global shared caches and isolated caches, and explain how different access levels
  affect cache storage and retrieval patterns.
repository: nrwl/nx
label: Caching
language: Markdown
comments_count: 2
repository_stars: 27518
---

When documenting caching systems, clearly specify cache isolation boundaries and access scopes to prevent confusion about cache behavior. Distinguish between global shared caches and isolated caches, and explain how different access levels affect cache storage and retrieval patterns.

For example, when describing read-only access tokens:
```markdown
The `read-only` access tokens can only read from the global remote cache. Task results produced with this type of access token will be stored in an isolated remote cache accessible _only_ by that specific branch in a CI context, and cannot influence the global shared cache. The isolated remote cache is accessible to all machines or agents in the same CI execution, enabling cache sharing during distributed task execution.
```

This approach helps developers understand:
- Which cache layer their operations will affect
- The scope of cache accessibility (global vs isolated)
- How cache isolation prevents unauthorized cache pollution
- When cache sharing is still possible within defined boundaries