---
title: Canonical naming consistency
description: 'Use canonical, consistently normalized identifiers across layers so
  the same concept is easily verifiable in code.


  Apply this in two ways:

  1) Match existing consumer normalization (e.g., whitespace handling) where the system
  already expects it.'
repository: ClInE/cLiNe
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70838
---

Use canonical, consistently normalized identifiers across layers so the same concept is easily verifiable in code.

Apply this in two ways:
1) Match existing consumer normalization (e.g., whitespace handling) where the system already expects it.
2) For repeated concepts (commands, icons, components), use the canonical symbol/import so a reader can confirm sameness by inspection.
3) Don’t silently “make valid” fundamentally broken identifiers—if an identifier is invalid by contract, treat it as a broken producer (don’t mask it with extra permissive validation).

Example patterns:
- Normalize inputs to match the consumer’s expected form, but don’t add broad “auto-fixing” beyond that.
```ts
// Normalize exactly as the runner expects (e.g., whitespace).
const normalizedMenuPath = menuPath.trim();
```
- Use a canonical icon/component import instead of ad-hoc duplicates so usage is verifiable.
```tsx
import { X } from "lucide-react";

export function CloseButton({ onClick }: { onClick: () => void }) {
  return <X className="h-4 w-4" onClick={onClick} aria-hidden />;
}
```