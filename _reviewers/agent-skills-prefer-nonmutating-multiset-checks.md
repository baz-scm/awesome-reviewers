---
title: Prefer nonmutating multiset checks
description: When doing algorithmic equality checks for arrays where order doesn’t
  matter (multiset equality), avoid (a) mutating the input with `.sort()` and (b)
  sort+join/stringify approaches when a linear-time counting strategy is available.
  Use a non-mutating sort (`toSorted`) only if sorting is truly the chosen approach;
  otherwise prefer counting maps (expected...
repository: vercel-labs/agent-skills
label: Algorithms
language: Markdown
comments_count: 2
repository_stars: 26385
---

When doing algorithmic equality checks for arrays where order doesn’t matter (multiset equality), avoid (a) mutating the input with `.sort()` and (b) sort+join/stringify approaches when a linear-time counting strategy is available. Use a non-mutating sort (`toSorted`) only if sorting is truly the chosen approach; otherwise prefer counting maps (expected O(n) in common JS engines) to avoid O(n log n) sorting.

Example (order-insensitive multiset equality):
```ts
function hasChanges(current: string[], original: string[]) {
  if (current.length !== original.length) return true;

  const counts = new Map<string, number>();
  for (const x of current) counts.set(x, (counts.get(x) ?? 0) + 1);
  for (const x of original) {
    const c = counts.get(x) ?? 0;
    if (c === 0) return true;
    if (c === 1) counts.delete(x);
    else counts.set(x, c - 1);
  }
  return counts.size !== 0;
}
```

If you must use sorting for comparison, use a non-mutating method:
```ts
return current.toSorted().join() !== original.toSorted().join();
```