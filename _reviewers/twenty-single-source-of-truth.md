---
title: Single source of truth
description: Establish a single authoritative source for each piece of data in your
  API interfaces rather than maintaining duplicate or parallel state. Derive computed
  values from the authoritative source instead of storing them separately.
repository: twentyhq/twenty
label: API
language: TSX
comments_count: 2
repository_stars: 35477
---

Establish a single authoritative source for each piece of data in your API interfaces rather than maintaining duplicate or parallel state. Derive computed values from the authoritative source instead of storing them separately.

When designing component interfaces, identify what should be the canonical source of truth and derive other values from it. This prevents inconsistencies and reduces complexity.

For example, instead of storing both headers and bodyType separately:

```typescript
// Avoid: Maintaining parallel state
type BodyInputProps = {
  headers: Record<string, string>;
  bodyType: BodyType; // Duplicate information
  onChange: (value?: string, isBodyType?: boolean) => void;
};

// Prefer: Single source of truth
type BodyInputProps = {
  headers: Record<string, string>; // Single source
  onChange: (value?: string) => void;
};

// Derive bodyType from headers when needed
const bodyType = deriveBodyTypeFromHeaders(headers);
```

Similarly, when accessing related data, prefer getting it from the authoritative source rather than relying on indirect indicators. Instead of checking `sourceHandleId`, get the actual source node to ensure type safety and accuracy.