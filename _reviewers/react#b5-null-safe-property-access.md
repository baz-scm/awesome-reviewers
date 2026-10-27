---
title: Null Safe Property Access
description: Before accessing properties/methods on a value that may be null/undefined
  (or of a different runtime shape), explicitly narrow to the correct state (or use
  a helper that already encodes the edge-cases). Don’t “hope” types/optional chaining
  match runtime behavior—branching should reflect the real platform invariants.
repository: facebook/react#b5
label: Null Handling
language: JavaScript
comments_count: 9
repository_stars: 251886
---

Before accessing properties/methods on a value that may be null/undefined (or of a different runtime shape), explicitly narrow to the correct state (or use a helper that already encodes the edge-cases). Don’t “hope” types/optional chaining match runtime behavior—branching should reflect the real platform invariants.

Apply this as a checklist:
- If the logic depends on object shape (e.g., node/document vs fragment), branch on node type and only then read shape-specific fields.
- If Flow types are unions/nullables, refine via type narrowing (or split handler types) so the guarded code sees a non-null/non-undefined type.
- Use existing “owner/document/root” helpers rather than duplicating ad-hoc casts.
- Keep null vs undefined consistent: ensure guards check the same representation your types use.
- Initialize nullable locals with an explicit null value (avoid `void | T` patterns that make nullability unclear).
- For refs/portals: if the container/ref is missing, early-return (treat “missing” as an expected state, not as something you’ll fix later).

Example pattern (node/document shape):
```js
const activeElementRoot = getHoistableRoot(parent);
const activeElement = (activeElementRoot: any).activeElement;
if (activeElement == null) {
  // safe: activeElement is genuinely null/undefined here
}
```

Example pattern (ref/portal early return):
```js
const hideMenu = portalContainer == null || items.length === 0;
useLayoutEffect(() => {
  if (hideMenu) return;
  const menu = menuRef.current;
  if (menu == null) return;
  // safe to use menu
}, [hideMenu]);
```

This standard prevents the common failure mode where code accesses a property that doesn’t exist for the current runtime shape, or where `null`/`undefined` are inconsistently modeled across types and guards.