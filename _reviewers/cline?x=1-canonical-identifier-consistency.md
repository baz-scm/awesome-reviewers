---
title: Canonical identifier consistency
description: When introducing or consuming named identifiers (command paths/names,
  UI component/icon identifiers), ensure they are *canonical* and *consistent* across
  all boundaries so the codebase is easy to verify.
repository: cline/cline?x=1
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70861
---

When introducing or consuming named identifiers (command paths/names, UI component/icon identifiers), ensure they are *canonical* and *consistent* across all boundaries so the codebase is easy to verify.

Apply two checks:
1) **Match the authoritative runtime normalization**: if the runner/runtime normalizes values (e.g., trimming), the producer (registration/composer/inspection) should apply the same normalization so names line up across registration/inspection/execution.
2) **Use canonical shared imports/components for shared assets**: if a package provides a standard named component (e.g., a Lucide icon), prefer that over inline/duplicated SVG so reviewers can reliably confirm the exact asset/component via imports.

Example (command/menu path normalization):
```ts
// ensure composer/inspection produces the same normalized menu path as the runner
const menuPath = rawMenuPath.trim();
// ...use menuPath for registration + inspection display
```

Example (canonical icon import):
```tsx
import { X } from 'lucide-react';

export function CloseIcon() {
  return <X className="h-4 w-4" />;
}
```