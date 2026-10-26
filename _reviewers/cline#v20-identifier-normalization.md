---
title: Identifier normalization
description: 'Ensure identifier-like strings and named assets use a single canonical
  representation across components.


  Apply this as two practical rules:


  1) Normalize before cross-boundary inspection/execution'
repository: cline/cline#v20
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70886
---

Ensure identifier-like strings and named assets use a single canonical representation across components.

Apply this as two practical rules:

1) Normalize before cross-boundary inspection/execution
- If a string is used as an identifier (menu path, command path/name, route, key, etc.), apply the same normalization the executor/runner uses (e.g., `trim()` for paths) *before* registration, inspection, or lookup.
- Don’t add validation rules in one pipeline stage if the system doesn’t enforce them elsewhere; treat truly invalid identifiers as broken producers.

2) Use consistent named imports/patterns for shared UI identifiers
- For commonly reused “named” assets (icons/components), prefer the shared import/component pattern so it’s easy to verify the same asset is used everywhere during code review.

Example (normalizing an identifier-like path):
```ts
const normalizedPath = rawPath.trim();
registerMenu({ path: normalizedPath, /* ... */ });
// Ensure any inspection/lookup uses the same normalization.
```

Example (use the same icon/component pattern everywhere):
```tsx
import { X } from 'lucide-react';

// Prefer a consistent usage pattern so code reviewers can easily confirm sameness.
<X className="h-4 w-4" />
```