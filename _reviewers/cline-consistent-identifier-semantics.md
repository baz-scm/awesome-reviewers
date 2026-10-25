---
title: Consistent identifier semantics
description: When code exposes an identifier outward—via UI semantics (ARIA) or via
  string-based integration points (paths/keys/command names)—make it match the contract
  expected by the consuming layer.
repository: CLINE/CLINE
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70837
---

When code exposes an identifier outward—via UI semantics (ARIA) or via string-based integration points (paths/keys/command names)—make it match the contract expected by the consuming layer.

Practical rules:
- UI controls: use semantic naming attributes (e.g., correct `role`, `aria-*` state, focusability) and ensure keyboard interaction corresponds to what the control “is”.
- Text identifiers: apply the same normalization (e.g., `trim()`, case rules, path canonicalization) everywhere the identifier is produced and consumed (registration, inspection, execution). Don’t “paper over” with mismatched local formatting.
- Centralize: put normalization in one helper (or the shared domain function) and call it from all call sites.

Example (path normalization applied consistently):
```ts
// Shared normalization contract
function normalizeMenuPath(path: string) {
  return path.trim();
}

// Use the same normalization when building UI paths and when the runner resolves them
const menuPath = normalizeMenuPath(rawMenuPath);
// ... later ...
const resolved = runnerResolve(normalizeMenuPath(menuPath));
```

Example (semantic naming for a UI control):
```tsx
<div
  role="separator"
  tabIndex={0}
  aria-valuemin={0}
  aria-valuenow={height}
  onKeyDown={(e) => {
    if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
      // resize based on the semantic intent of the control
    }
  }}
/>
```