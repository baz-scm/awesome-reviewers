---
title: Ancestor-stack cycle detection
description: When writing recursive algorithms that walk graph-like or tree-like data
  (deep clone, serialization, search), distinguish "this object is one of the current
  recursion's ancestors" (a real cycle) from "this object was visited somewhere else
  in the structure" (a legitimate shared/non-cyclic reference). Using a single global
  `WeakSet`/`Set` of visited nodes...
repository: promptfoo/promptfoo
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 26565
---

When writing recursive algorithms that walk graph-like or tree-like data (deep clone, serialization, search), distinguish "this object is one of the current recursion's ancestors" (a real cycle) from "this object was visited somewhere else in the structure" (a legitimate shared/non-cyclic reference). Using a single global `WeakSet`/`Set` of visited nodes conflates these two cases and silently corrupts output by replacing valid shared references (e.g., the same trace entry appearing in two summary arrays) with a `[Circular]`/`[Cycle omitted]` placeholder.

Instead, track ancestors as a per-branch stack that is pushed on entry to a node and popped on exit, so only true back-references along the current path are flagged:

```ts
function safeClone(value: unknown, ancestors: object[] = []): unknown {
  if (value === null || typeof value !== 'object') {
    return value;
  }
  // Real cycle: this object is already on the current path, not merely
  // visited elsewhere in the structure.
  if (ancestors.includes(value)) {
    return '[Circular]';
  }
  const nextAncestors = [...ancestors, value];
  if (Array.isArray(value)) {
    return value.map((item) => safeClone(item, nextAncestors));
  }
  const out: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
    out[k] = safeClone(v, nextAncestors);
  }
  return out;
}
```

Apply the same rigor to worst-case complexity when a recursive or regex-based scan runs on untrusted/large input: verify it can't degrade to quadratic or worse (e.g., an unbounded lazy regex rescanning from every unmatched delimiter). Prefer a single linear pass (explicit delimiter/index scanning) over clever but unbounded patterns, and add a regression test with a large/adversarial input to confirm linear behavior before merging. When bounding input size as a stopgap, make sure the bound doesn't silently produce wrong results for valid large inputs — fix the underlying complexity instead of truncating correctness.