---
title: Canonical Identifier Naming
description: 'Use a canonical, consistent form for identifiers so matching and auditing
  work reliably across layers.


  Apply this rule in two common cases:

  1) **String identifiers (command/menu paths, IDs):** Normalize to the system’s canonical
  representation at the boundary where strings enter (e.g., apply `trim()` if the
  runner normalizes). Don’t invent new restrictions...'
repository: cline/cline#v22
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70886
---

Use a canonical, consistent form for identifiers so matching and auditing work reliably across layers.

Apply this rule in two common cases:
1) **String identifiers (command/menu paths, IDs):** Normalize to the system’s canonical representation at the boundary where strings enter (e.g., apply `trim()` if the runner normalizes). Don’t invent new restrictions in one layer if other layers don’t enforce them.

```ts
// Normalize to match runner canonicalization
const canonicalPath = rawPath.trim();
registerCommand({ name: canonicalPath, ... });
// Ensure inspection/execution uses the same canonical form
```

2) **Symbol identifiers (UI assets like icons):** Prefer the canonical named import/component usage pattern for repeated assets so the codebase is auditable and consistent (making it easy to verify “are we using the same icon everywhere?”).

```tsx
// Prefer consistent icon component usage pattern
import { X } from "lucide-react";

function CloseButton() {
  return <X className="h-4 w-4" />;
}
```

Net effect: reviewers can quickly verify identifier consistency, and runtime behavior doesn’t depend on subtle string/symbol mismatches.