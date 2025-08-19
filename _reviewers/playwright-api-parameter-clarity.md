---
title: API parameter clarity
description: Design API parameters to be self-documenting and minimize cognitive overhead.
  Avoid boolean parameters in favor of descriptive enums or string literals, leverage
  type inference where possible, and prefer clean parameter passing over state mutation
  patterns.
repository: microsoft/playwright
label: API
language: TypeScript
comments_count: 5
repository_stars: 76113
---

Design API parameters to be self-documenting and minimize cognitive overhead. Avoid boolean parameters in favor of descriptive enums or string literals, leverage type inference where possible, and prefer clean parameter passing over state mutation patterns.

Key principles:
- Replace boolean flags with descriptive string literals or enums that clearly indicate behavior
- Implement automatic type/parameter inference when context provides sufficient information
- Pass new values as parameters rather than mutating state and rolling back on failure
- Remove redundant parameters when all callers use the same value

Example of boolean parameter improvement:
```typescript
// Instead of:
async function processSnapshot(updateIndex: boolean) {
  // unclear what true/false means
}

// Use descriptive options:
async function processSnapshot(indexBehavior: 'updateAnonymousSnapshotIndex' | 'dontUpdateAnonymousSnapshotIndex') {
  // behavior is immediately clear
}
```

Example of parameter inference:
```typescript
// Instead of requiring explicit contentType:
await testInfo.attach('report.html', { 
  path: attachmentFile, 
  contentType: 'text/html' // redundant
});

// Infer from file extension:
await testInfo.attach('report.html', { 
  path: attachmentFile // contentType inferred from .html extension
});
```

This approach reduces API surface area, prevents misuse, and makes code more maintainable by encoding intent directly in the parameter names and types.