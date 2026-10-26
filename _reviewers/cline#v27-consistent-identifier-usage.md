---
title: Consistent Identifier Usage
description: 'When a value is used as an identifier (command names, menu paths, icons/components),
  keep it consistent and recognizable end-to-end:


  1) **Match normalization rules across stages**: If downstream code normalizes (e.g.,
  `trim()`), apply the same normalization at registration/lookup time. Avoid introducing
  new validation in only one part of the pipeline if...'
repository: cline/cline#v27
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70892
---

When a value is used as an identifier (command names, menu paths, icons/components), keep it consistent and recognizable end-to-end:

1) **Match normalization rules across stages**: If downstream code normalizes (e.g., `trim()`), apply the same normalization at registration/lookup time. Avoid introducing new validation in only one part of the pipeline if other parts don’t enforce it.

2) **Use the canonical named source for shared identifiers**: For repeated UI/icon identifiers, prefer importing and using the standard named component (so it’s obvious in code which icon/component is used) instead of duplicating inline markup that makes consistency hard to verify.

Example (normalization consistency):
```ts
function normalizeMenuPath(path: string) {
  return path.trim(); // align with runner normalization
}

// apply normalizeMenuPath consistently wherever the name/path is compared or emitted
```

Example (canonical named icon usage):
```tsx
import { X } from "lucide-react";

export function CloseButton({ onClick }: { onClick: () => void }) {
  return (
    <button type="button" onClick={onClick} aria-label="Close">
      <X className="h-4 w-4" />
    </button>
  );
}
```