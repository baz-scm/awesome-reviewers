---
title: Canonical Naming Consistency
description: For any externally visible identifiers (command names, icon components,
  etc.), enforce a single canonical naming/formatting approach and make it easy to
  verify in code.
repository: cline/cline#v6
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70864
---

For any externally visible identifiers (command names, icon components, etc.), enforce a single canonical naming/formatting approach and make it easy to verify in code.

- Normalize names exactly as the execution layer expects (e.g., trim whitespace) so inspection/registration/execution don’t diverge.
- Keep validation rules aligned with what the actual runner/CLI enforces—avoid “extra” naming validation in one phase if it isn’t enforced everywhere.
- Prefer canonical, shared identifier sources (standard imports/components) over ad-hoc/unique patterns, so reviewers can quickly confirm consistency.

Example (normalizing an identifier before inspection/registration):
```ts
// Canonicalize once, then reuse.
const canonicalMenuPath = menuPath.trim();

// Use canonicalMenuPath consistently across registration + inspection + execution.
registerCommand({ menuPath: canonicalMenuPath, /* ... */ });
inspectCommand({ menuPath: canonicalMenuPath });
executeCommand({ menuPath: canonicalMenuPath });
```

Example (consistent icon identifier usage):
```tsx
// Prefer a single, canonical lucide import/component pattern across the package.
import { X } from "lucide-react";

export function CloseButton({ onClick }: { onClick: () => void }) {
  return <X className="h-4 w-4" onClick={onClick} />;
}
```