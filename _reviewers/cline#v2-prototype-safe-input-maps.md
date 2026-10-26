---
title: Prototype-Safe Input Maps
description: Treat any externally derived values (file paths/extensions, names, identifiers)
  and UI-triggering events as untrusted. When resolving behavior from string keys,
  use prototype-safe lookups so inherited properties like `__proto__`/`constructor`
  can’t alter control flow.
repository: cline/cline#v2
label: Security
language: TSX
comments_count: 3
repository_stars: 70861
---

Treat any externally derived values (file paths/extensions, names, identifiers) and UI-triggering events as untrusted. When resolving behavior from string keys, use prototype-safe lookups so inherited properties like `__proto__`/`constructor` can’t alter control flow.

**Do**
- Use `Object.hasOwn` (or `Map`) for lookups in plain objects keyed by untrusted strings.
- Always provide a safe neutral fallback for unknown keys.
- For security-sensitive UI actions bound to keyboard shortcuts, stop unintended handlers from processing the same event.

**Example: prototype-safe mapping**
```ts
type Spec = { icon: unknown; className: string };
const BY_EXT: Record<string, Spec> = { ts: { icon: 'code', className: '...' } };

export function specForExt(ext: string): Spec {
  const key = ext.toLowerCase();
  return Object.hasOwn(BY_EXT, key) ? BY_EXT[key] : { icon: 'neutral', className: 'text-muted-foreground' };
}
```

**Example: contain sensitive keyboard actions**
```ts
function onKeyDown(event: KeyboardEvent) {
  if (!matchesAccelerator(event, accelerator)) return;
  event.preventDefault();
  event.stopImmediatePropagation();
  // perform the security-sensitive action
}
```

**Why**
- Prevents prototype/inherited-property edge cases from changing lookup behavior.
- Reduces risk of unintended components receiving security-relevant input (e.g., shortcut collisions).