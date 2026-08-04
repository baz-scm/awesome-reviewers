---
title: Use Correct Null Semantics
description: 'Treat “missing/unknown” differently from “present/true” and from “known
  false”. Two common pitfalls:


  1) CLI flags: frameworks may represent valueless options as the string `"true"`,
  which breaks guards that only check truthiness.'
repository: awslabs/aidlc-workflows
label: Null Handling
language: TypeScript
comments_count: 2
repository_stars: 3849
---

Treat “missing/unknown” differently from “present/true” and from “known false”. Two common pitfalls:

1) CLI flags: frameworks may represent valueless options as the string `"true"`, which breaks guards that only check truthiness.
   - Standard: For flags that require a meaningful value, explicitly validate allowed values (non-empty, non-"true", matches expected format) and treat `"true"` as absent.

2) Nullable/tri-state functions: returning `false` where the caller expects `null` (or vice versa) silently changes control flow and fallback behavior.
   - Standard: Use `null` to mean “cannot determine/should fall back”, and return `false` only when you have a definitive negative after successful checks. Callers must branch on `=== null` (not falsiness).

Example (pattern):
```ts
// 1) CLI normalization for value-bearing flags
function flagValue(v: unknown): string | undefined {
  if (typeof v !== "string") return undefined;
  const t = v.trim();
  // parseArgs may produce "true" for valueless options
  if (!t || t === "true") return undefined;
  return t;
}

const scope = flagValue(flags.scope);
const argumentsDesc = flagValue(flags.arguments);
const label = flagValue(flags.label);

if (!scope && !argumentsDesc && !label) {
  throw new Error("Fail-closed: missing required intent descriptors");
}

// 2) Tri-state function contract
function gitHasSourceWork(pd: string): boolean | null {
  const lastCommit = /* git diff ... */ null as string | null;
  if (lastCommit === null) return null;   // unknown -> caller should fall back
  // inspected successfully and definitively negative:
  return false;
}

const r = gitHasSourceWork(pd);
if (r === null) {
  // fallback probe
} else if (r) {
  // allow
} else {
  // refuse
}
```

Apply this standard anywhere you:
- validate optional inputs (CLI flags, env vars, JSON fields), or
- rely on nullable contracts for control-flow (fallbacks, short-circuiting, “unknown” vs “definitely false”).