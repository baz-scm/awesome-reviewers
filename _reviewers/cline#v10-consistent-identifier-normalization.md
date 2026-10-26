---
title: Consistent Identifier Normalization
description: 'Use a single, shared convention for how identifiers are formatted and
  sourced across the codebase.


  - **Normalize names the same way everywhere** they’re produced and consumed (e.g.,
  command/menu paths). Don’t add validation in only one layer; if the system currently
  allows certain forms, keep that behavior consistent across registration, inspection,
  and...'
repository: cline/cline#v10
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70869
---

Use a single, shared convention for how identifiers are formatted and sourced across the codebase.

- **Normalize names the same way everywhere** they’re produced and consumed (e.g., command/menu paths). Don’t add validation in only one layer; if the system currently allows certain forms, keep that behavior consistent across registration, inspection, and execution.
- **Use canonical imports/symbols for named UI elements** (icons/components). Prefer using the same exported component (or shared icon import) so that it’s easy to verify consistency by code inspection; avoid duplicating one-off inline SVGs when a standard icon component exists.

Example (command/menu path normalization):
```ts
// Wherever you create or compare command/menu paths:
const normalizedPath = rawPath.trim();
registerCommand(normalizedPath, handler);
inspectCommand(normalizedPath);
executeCommand(normalizedPath);
```

Example (canonical icon usage):
```tsx
// Prefer the same imported icon component the rest of the package uses.
import { X } from 'lucide-react';

export function CloseButton({ onClose }: { onClose: () => void }) {
  return (
    <button type="button" onClick={onClose} aria-label="Close">
      <X className="h-4 w-4" />
    </button>
  );
}
```