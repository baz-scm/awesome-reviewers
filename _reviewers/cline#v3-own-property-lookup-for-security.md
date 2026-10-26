---
title: Own-property lookup for security
description: 'When behavior depends on user-controlled strings (file paths, extensions,
  names, etc.), treat them as untrusted input: perform *own-property* lookups and
  fall back to a neutral default instead of allowing prototype-chain keys (e.g., `__proto__`,
  `constructor`). Also, for security-related settings, make the allowed actions and
  execution context unambiguous...'
repository: cline/cline#v3
label: Security
language: TSX
comments_count: 3
repository_stars: 70863
---

When behavior depends on user-controlled strings (file paths, extensions, names, etc.), treat them as untrusted input: perform *own-property* lookups and fall back to a neutral default instead of allowing prototype-chain keys (e.g., `__proto__`, `constructor`). Also, for security-related settings, make the allowed actions and execution context unambiguous (e.g., read vs write; background executor vs integrated terminal).

**Coding rule (prototype-safe maps):**
- Use `Object.hasOwn(map, key)` (or `Object.prototype.hasOwnProperty.call`) before reading from a plain object used as a lookup table.
- Always define a safe default for unknown keys.

**Example:**
```ts
type IconSpec = { icon: unknown; className: string };
const BY_EXTENSION: Record<string, IconSpec> = { ts: { icon: {}, className: 'text-sky-600' } };
const NEUTRAL: IconSpec = { icon: {}, className: 'text-muted-foreground' };

function specForPath(path: string): IconSpec {
  const name = path.split(/[\\/]/).pop() ?? path;
  const extension = name.includes('.') ? name.split('.').pop()!.toLowerCase() : '';
  return Object.hasOwn(BY_EXTENSION, extension) ? BY_EXTENSION[extension] : NEUTRAL;
}
```

**Security UI rule:**
- If a setting affects sandboxing/permissions, the description must clearly distinguish what remains possible (e.g., read anywhere) vs what is restricted (e.g., write/command execution only within the project) and where commands run (background executor vs integrated terminal).
