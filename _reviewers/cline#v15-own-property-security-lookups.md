---
title: Own-Property Security Lookups
description: When you map untrusted input (e.g., file paths/names/extensions) to security-
  or behavior-relevant tables, only accept *own* properties on the lookup object—do
  not allow inherited/prototype keys like `__proto__`, `constructor`, or `toString`
  to be treated as valid matches. Also, for permission/sandbox features, ensure the
  UI text precisely reflects...
repository: cline/cline#v15
label: Security
language: TSX
comments_count: 3
repository_stars: 70877
---

When you map untrusted input (e.g., file paths/names/extensions) to security- or behavior-relevant tables, only accept *own* properties on the lookup object—do not allow inherited/prototype keys like `__proto__`, `constructor`, or `toString` to be treated as valid matches. Also, for permission/sandbox features, ensure the UI text precisely reflects enforcement boundaries (e.g., broad read capability vs restricted command write capability, and whether execution occurs in the background executor vs the integrated terminal).

Practical rules:
- For dictionaries used for lookups from untrusted strings, check with `Object.hasOwn(lookup, key)` before using `lookup[key]`.
- Prefer `Record<string, T>` plus own-property checks when falling back to a neutral/default behavior.
- For sandboxed settings, write copy that distinguishes: (1) what tools can do (read scope) vs (2) what commands can do (write/modify scope) and (3) the execution surface (background executor vs terminal).

Example (own-property lookup hardening):
```ts
type IconSpec = { icon: unknown; className: string };
const BY_EXTENSION: Record<string, IconSpec> = { ts: { icon: null, className: "" } };
const NEUTRAL: IconSpec = { icon: null, className: "text-muted-foreground" };

function lookupByExtension(path: string): IconSpec {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.includes(".") ? (name.split(".").pop() ?? "").toLowerCase() : "";
  if (Object.hasOwn(BY_EXTENSION, ext)) return BY_EXTENSION[ext];
  return NEUTRAL;
}
```

Example (security-copy requirement):
- Explicitly say something like: “Read access remains broad via file tools, but command execution can only modify files within the current project,” and “commands run in the background executor (not the integrated terminal) while this setting is enabled.”