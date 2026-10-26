---
title: Canonical Naming Consistency
description: 'Use a single canonical form for any named identifier or UI asset so
  it’s consistent and easy to verify across the codebase.


  - For string-based “names” that must match elsewhere (paths, command/menu labels,
  etc.), normalize them the same way at every boundary where they’re compared or emitted
  (e.g., registration vs. runner/inspection). Apply only the...'
repository: cline/cline#v15
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70877
---

Use a single canonical form for any named identifier or UI asset so it’s consistent and easy to verify across the codebase.

- For string-based “names” that must match elsewhere (paths, command/menu labels, etc.), normalize them the same way at every boundary where they’re compared or emitted (e.g., registration vs. runner/inspection). Apply only the normalization that the system itself expects; don’t add extra validation/behavior unless execution enforces it.
- For named UI assets/components (e.g., icons), standardize the import/usage pattern so reviewers can quickly confirm that the same asset is used (avoid ad-hoc inline/alternate patterns when a shared component exists).

Example (string normalization boundary):
```ts
// Ensure menu path matches runner normalization
const menuPath = rawMenuPath.trim();
// Use menuPath consistently for registration + inspection + execution lookup
registerMenu({ path: menuPath, ... });
inspectMenu({ path: menuPath });
executeMenu({ path: menuPath });
```

Example (consistent asset naming):
```tsx
import { X } from 'lucide-react';

// Prefer the same canonical component usage pattern everywhere
<X className="h-4 w-4" aria-hidden />
```

This improves matching correctness (no hidden whitespace/format drift) and makes identifier/asset audits simpler during reviews.