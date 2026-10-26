---
title: Standardize identifier usage
description: 'Ensure identifiers (command names, menu paths, shared UI assets/icons,
  etc.) are handled in a consistent, auditable way across the codebase.


  - Apply the same normalization rules anywhere an identifier is compared, looked
  up, or displayed. If one boundary normalizes (e.g., the runner), the producer/composer
  should normalize too (e.g., `trim()`), so names...'
repository: cline/cline#v7
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70865
---

Ensure identifiers (command names, menu paths, shared UI assets/icons, etc.) are handled in a consistent, auditable way across the codebase.

- Apply the same normalization rules anywhere an identifier is compared, looked up, or displayed. If one boundary normalizes (e.g., the runner), the producer/composer should normalize too (e.g., `trim()`), so names match deterministically.
- Use canonical, named sources for shared identifiers/assets. If a shared icon exists (e.g., a Lucide `X` export), prefer importing and using the standard component rather than embedding a custom/inconsistent inline SVG, so reviewers can reliably verify consistency via imports/search.
- Avoid “papering over” invalid identifiers with new, inconsistent validation if other layers don’t enforce it; treat mismatches as a broken integration and keep the rules consistent across registration/inspection/execution.

Example (normalization):
```ts
const normalizedPath = menuPath.trim();
// use normalizedPath consistently for comparisons/lookups
``` 

Example (canonical icon usage):
```tsx
import { X } from 'lucide-react';

function CloseButton({ onClose }: { onClose: () => void }) {
  return (
    <button type="button" onClick={onClose}>
      <X className="h-4 w-4" />
    </button>
  );
}
```