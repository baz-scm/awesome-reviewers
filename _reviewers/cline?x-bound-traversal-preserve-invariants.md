---
title: Bound traversal, preserve invariants
description: When an algorithm pages through, indexes into, or traverses a collection
  that can be mutated mid-flight or can contain cycles (sliced/paginated lists, symlink
  graphs, recursive trees), treat index/cursor adjustment and cycle/termination bounds
  as first-class correctness requirements, not afterthoughts.
repository: cline/cline?x
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 70983
---

When an algorithm pages through, indexes into, or traverses a collection that can be mutated mid-flight or can contain cycles (sliced/paginated lists, symlink graphs, recursive trees), treat index/cursor adjustment and cycle/termination bounds as first-class correctness requirements, not afterthoughts.

- For indexed or paginated collections, removing/skipping an item before the current cursor must shift the cursor so the visible window doesn't jump; identities (ids) assigned to items should be stable across re-slicing so external state (highlights, undo, "skip" targeting) keeps pointing at the right element even as the underlying pool changes.
- For recursive or graph-like traversals (e.g., following symlinks, expanding directories, resolving references), explicitly detect cycles (a target that is `.`, `..`, or an ancestor already on the current chain) and cap the total number of expansions/recursion depth, so a malicious or accidental cycle degrades to "skipped and reported" rather than an infinite loop or combinatorial blowup.
- Lock these invariants down with tests that go beyond a single example: pin a concrete regression case (e.g., "skip the row before the cursor, new set still shows the same visible rows") and, where the state space is large (sequences of user actions, arbitrary link graphs), add a property-based/fuzz test that asserts the invariant itself (e.g., "skip hides only its row", "`more` drops only the last row") rather than one hand-picked trace.

Example shape for cycle-safe expansion with a hard cap:

```ts
function addLinked(path: string, target: string, depth: number) {
  const resolved = resolve(path, target);
  if (isCycle(resolved, currentChain) || depth > MAX_LINK_DEPTH || expansions++ > MAX_LINK_EXPANSIONS) {
    skippedPaths.push(path);
    return;
  }
  // ...expand resolved, recursing with depth + 1
}
```

Applying this consistently prevents a class of bugs where paging/removal logic silently shifts the user's view, external references go stale, or a cyclic structure causes unbounded work.