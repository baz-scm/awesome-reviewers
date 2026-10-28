---
title: Guard against prototype pollution lookups
description: When indexing into plain JavaScript/TypeScript objects using keys derived
  from external or user-controlled input (e.g., file names, extensions, folder names),
  never rely on direct bracket access like `map[key]`. Untrusted keys such as "constructor",
  "__proto__", "toString", or "hasOwnProperty" will resolve to inherited properties
  on `Object.prototype`...
repository: 'cline/cline

  '
label: Security
language: TSX
comments_count: 1
repository_stars: 70942
---

When indexing into plain JavaScript/TypeScript objects using keys derived from external or user-controlled input (e.g., file names, extensions, folder names), never rely on direct bracket access like `map[key]`. Untrusted keys such as "constructor", "__proto__", "toString", or "hasOwnProperty" will resolve to inherited properties on `Object.prototype` instead of `undefined`, causing unexpected behavior or potential prototype-pollution-style exploits.

Always verify the key is an own property before accessing it, using `Object.hasOwn(obj, key)` (or `Object.prototype.hasOwnProperty.call`), and fall back to a safe default when it is not an own property. Prefer `Map` over plain objects for untrusted-key lookups when feasible, since `Map` has no prototype chain to leak.

Example fix:
```ts
function lookup(table: Record<string, IconSpec>, key: string): IconSpec | undefined {
  return Object.hasOwn(table, key) ? table[key] : undefined;
}

export function fileIconSpec(path: string): IconSpec {
  const name = baseName(path).toLowerCase();
  const byName = lookup(BY_NAME, name);
  if (byName) return byName;
  // ... same guarded pattern for BY_EXTENSION and BY_FOLDER
  return DEFAULT_ICON;
}
```

Add regression tests covering malicious/edge-case keys (e.g., `"constructor"`, `"__proto__"`, `"x.constructor"`) to confirm they resolve to the safe default rather than an inherited object method.</description>
