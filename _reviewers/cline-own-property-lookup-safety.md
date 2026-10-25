---
title: Own-Property Lookup Safety
description: When using user-derived strings (e.g., paths, filenames, extensions)
  to index plain JS objects as lookup tables, do not rely on inherited properties
  from the prototype chain. Use own-property checks (or `Map`) and add tests for malicious
  keys.
repository: CLINE/CLINE
label: Security
language: TSX
comments_count: 3
repository_stars: 70837
---

When using user-derived strings (e.g., paths, filenames, extensions) to index plain JS objects as lookup tables, do not rely on inherited properties from the prototype chain. Use own-property checks (or `Map`) and add tests for malicious keys.

**Standard**
- For dictionary-style objects, prefer:
  - `Object.hasOwn(dict, key)` before using `dict[key]`, or
  - a `Map` keyed by strings.
- Treat keys like `"__proto__"`, `"constructor"`, `"toString"`, and `"prototype"` as security test cases.
- If a security setting constrains permissions (read vs write, sandbox vs terminal), ensure the UI text clearly states the boundary and execution context (especially for OS-specific behavior).

**Example (object + own-property check)**
```ts
type IconSpec = { icon: unknown; className: string };
const BY_EXTENSION: Record<string, IconSpec> = {
  ts: { icon: {}, className: "text-sky-600" },
};

function iconForPath(path: string): IconSpec {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.includes(".") ? (name.split(".").pop() ?? "").toLowerCase() : "";

  // Security: avoid inherited/prototype-chain keys being treated as valid.
  if (Object.hasOwn(BY_EXTENSION, ext)) return BY_EXTENSION[ext];

  // neutral fallback
  return { icon: {}, className: "text-muted-foreground" };
}
```

**Tests to add**
- Assert safe fallback behavior when `path` yields keys like `__proto__`, `constructor`, or `toString`.
- (Security UX) Verify the setting description distinguishes “can read” vs “can change/execute” and the actual execution context when relevant.