---
title: consistent nullable returns
description: Establish consistent patterns for nullable return values in APIs and
  document them clearly. Use `null` consistently for "not found" or "unavailable"
  cases rather than mixing `null`, `undefined`, and `false`. Always document when
  and why nullable values are returned, explaining the specific conditions that lead
  to these values.
repository: electron/electron
label: Null Handling
language: Markdown
comments_count: 4
repository_stars: 117644
---

Establish consistent patterns for nullable return values in APIs and document them clearly. Use `null` consistently for "not found" or "unavailable" cases rather than mixing `null`, `undefined`, and `false`. Always document when and why nullable values are returned, explaining the specific conditions that lead to these values.

For return type documentation, specify the nullable type and provide clear explanations:

```typescript
// Good: Consistent use of null with clear documentation
Returns `WebContents | null` - The `WebContents` owned by this view 
or `null` if the contents are destroyed.

Returns `WebFrameMain | null` - A frame with the given process and frame token,
or `null` if there is no WebFrameMain associated with the given IDs.

// Avoid: Mixing null, undefined, and false inconsistently
Returns `string | false` // when documented as `string | null`
Returns `ServiceWorkerMain | undefined` // when other APIs use `null`
```

Ensure implementation matches documentation - if the docs specify `string | null`, the implementation should return `null`, not `false` or `undefined`. This consistency helps developers understand and handle edge cases predictably across the entire API surface.