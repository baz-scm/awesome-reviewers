---
title: Strict Null Safety Checks
description: 'Adopt a consistent “strict null safety” approach:


  - **Derive from the correct owning/root object** before reading properties that
  may be retargeted (e.g., DOM `activeElement` inside shadow trees). Don’t assume
  `ownerDocument` is always valid for the node you’re holding.'
repository: facebook/react#b10
label: Null Handling
language: JavaScript
comments_count: 6
repository_stars: 251894
---

Adopt a consistent “strict null safety” approach:

- **Derive from the correct owning/root object** before reading properties that may be retargeted (e.g., DOM `activeElement` inside shadow trees). Don’t assume `ownerDocument` is always valid for the node you’re holding.
- **Guard before calling methods / reading properties** on values that can be `null`/`undefined` (refs, optional display names, etc.).
- **Use clear null comparisons** (`=== null` / `!== null`), and avoid `== null` unless you explicitly want to treat `null` and `undefined` equivalently.
- **Fail fast for impossible states**: if your types imply a value can’t be null but code must handle it, prefer an explicit error over silently continuing with optional-chaining.

Example patterns:

```js
// 1) Read from the correct root (DOM/shadow-safe)
const activeElementRoot = getHoistableRoot(parentInstanceOrContainer);
const activeElement = activeElementRoot.activeElement;
if (activeElement == null) {
  // ...handle missing active element
}
```

```js
// 2) Guard refs before use
const menu = ref.current;
if (menu === null) {
  return;
}
menu.classList.add('open');
```

```js
// 3) Guard before calling methods
let displayName = showNames ? agent.getComponentNameForHostInstance(node) : null;
if (displayName !== null && displayName.startsWith('Forget(')) {
  displayName = '✨' + displayName.slice(7, -1);
}
```

```js
// 4) Prefer crashing over masking impossible nulls
if (next.next === null) {
  throw new Error('Unexpected hook shape: useSyncExternalStore internal node missing');
}
```

Applying these rules will reduce null/undefined reference crashes and prevent incorrect assumptions about where null-sensitive data originates.