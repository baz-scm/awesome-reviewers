---
title: Maintain API version compatibility
description: When implementing or modifying APIs, ensure backward compatibility across
  versions and client interfaces. Carefully evaluate field structures, method visibility,
  and response formats for consistency.
repository: grafana/grafana
label: API
language: TypeScript
comments_count: 3
repository_stars: 68825
---

When implementing or modifying APIs, ensure backward compatibility across versions and client interfaces. Carefully evaluate field structures, method visibility, and response formats for consistency.

When fields differ between API versions:
```typescript
// Instead of directly checking version-specific fields
if (fromCache && fromCache.state.version === rsp?.dashboard.version) {
  // ...
}

// Use a more robust check that works across API versions
if (fromCache && fromCache.state.meta.updated === rsp?.meta.updated) {
  // ...
}
```

Before making methods private or changing signatures, verify there are no external consumers. Generate API clients in a way that accommodates both open source and enterprise code organization. When supporting multiple API versions (e.g., v1, v2, beta), implement fallback mechanisms and thoroughly test each version with appropriate feature toggles.

Document any breaking changes clearly, including migration paths for consumers. Consider providing adapter patterns or polyfills during transition periods to ease adoption of new API versions.