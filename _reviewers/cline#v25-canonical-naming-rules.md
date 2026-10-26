---
title: Canonical Naming Rules
description: When you work with named identifiers (command names/paths, or shared
  UI symbols like icons), make them consistently canonical so code is easy to audit.
repository: cline/cline#v25
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70891
---

When you work with named identifiers (command names/paths, or shared UI symbols like icons), make them consistently canonical so code is easy to audit.

Apply two checks:
1) **Match normalization to the execution path**: if the runner/executor normalizes values (e.g., `trim()`), apply the same normalization wherever you compare/build/inspect those names.
2) **Use canonical named sources for shared symbols**: prefer the same shared component/import pattern (e.g., the same `lucide` icon component) instead of mixing inline SVGs or divergent symbol definitions, so readers can quickly verify you’re using the intended symbol.

Example (normalization parity):
```ts
// Ensure menu/command path strings match runner normalization
const normalized = menuPath.trim();
// build/compare using `normalized` consistently
```

Example (canonical icon usage):
```tsx
// Prefer a consistent icon component import across the UI package
import { X } from "lucide-react";

export function CloseButton({ onClick }: { onClick: () => void }) {
  return (
    <button type="button" onClick={onClick}>
      <X className="h-4 w-4" />
    </button>
  );
}
```