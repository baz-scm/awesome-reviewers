---
title: Safe map lookups
description: When deriving behavior from untrusted strings (e.g., file paths, filenames,
  extensions, or any input that can be user-controlled), only consult lookup tables
  by *own keys* and use a safe default for unknown values. This prevents prototype-chain
  keys like `__proto__`, `constructor`, and `toString` from being used.
repository: cline/cline#v27
label: Security
language: TSX
comments_count: 3
repository_stars: 70892
---

When deriving behavior from untrusted strings (e.g., file paths, filenames, extensions, or any input that can be user-controlled), only consult lookup tables by *own keys* and use a safe default for unknown values. This prevents prototype-chain keys like `__proto__`, `constructor`, and `toString` from being used.

Also ensure security-relevant settings/UI copy precisely matches the actual authorization boundary and execution context (e.g., “tools can read; sandboxed commands can’t write outside the project”, and whether actions run in the background executor vs an integrated terminal).

Example (own-key lookup + safe fallback):

```ts
type IconSpec = { icon: string; className: string };

const BY_EXTENSION: Record<string, IconSpec> = {
  ts: { icon: "FileCode2", className: "text-sky-600" },
  json: { icon: "Braces", className: "text-amber-600" },
};

export function iconSpecFromPath(path: string): IconSpec {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.includes(".") ? (name.split(".").pop() ?? "").toLowerCase() : "";

  const key = ext;
  return Object.hasOwn(BY_EXTENSION, key) ? BY_EXTENSION[key] : { icon: "FileText", className: "text-muted" };
}
```

Standardize this pattern anywhere you map untrusted input → behavior/attributes (including language highlighters and policy-related UI/logic), and verify with tests for `__proto__`/`constructor`-style inputs.