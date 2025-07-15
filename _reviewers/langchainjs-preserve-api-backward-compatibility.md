---
title: Preserve API backward compatibility
description: When modifying existing APIs, maintain backward compatibility by implementing
  changes in a non-breaking way. Use method overloading, optional parameters, or deprecation
  notices rather than direct breaking changes.
repository: langchain-ai/langchainjs
label: API
language: TypeScript
comments_count: 7
repository_stars: 15004
---

When modifying existing APIs, maintain backward compatibility by implementing changes in a non-breaking way. Use method overloading, optional parameters, or deprecation notices rather than direct breaking changes.

Example of proper API evolution:

```typescript
// Instead of changing existing interface:
interface DeleteParams {
  ids: string[];
}

// Add overloaded method signatures:
class Store {
  // Original method
  async delete(ids: string[]): Promise<void>;
  // New overload with expanded functionality
  async delete(params: DeleteParams): Promise<void>;
  // Implementation handling both cases
  async delete(idsOrParams: string[] | DeleteParams): Promise<void> {
    if (Array.isArray(idsOrParams)) {
      // Handle legacy case
      return this.deleteByIds(idsOrParams);
    }
    // Handle new case
    return this.deleteWithParams(idsOrParams);
  }
}

// For deprecations, add clear notices:
/** @deprecated Use newMethod() instead. Will be removed in next major version. */
```

This approach allows gradual migration to new patterns while maintaining existing integrations. When deprecating functionality, provide clear migration paths and timeline in documentation.
