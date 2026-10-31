---
title: Iterative, cycle-safe traversal
description: 'When walking graph or tree structures whose depth or shape is attacker/user
  controlled (JSON-like payloads, recall graphs, nested message content), avoid naive
  recursive walks and naive cycle checks — both degrade from an engineering bug into
  an algorithmic complexity bug:'
repository: can1357/oh-my-pi
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 37317
---

When walking graph or tree structures whose depth or shape is attacker/user controlled (JSON-like payloads, recall graphs, nested message content), avoid naive recursive walks and naive cycle checks — both degrade from an engineering bug into an algorithmic complexity bug:

1. Use an explicit worklist/stack instead of recursion. A JS stack frame per nesting level overflows on deeply nested but perfectly valid input (chains tens of thousands of levels deep were observed crashing persistence that must otherwise just reject the input). Rewrite recursive walks as iterative loops with an explicit pending-items array.

2. Detect cycles with O(1) membership checks, not O(depth) ancestor scans. Walking up a linked "parent" chain to check "is this node already on my path" turns an otherwise linear walk into O(n²) on deep acyclic input. Track the current path in a `Set`/hash-map keyed by object identity, add a node when entering it, remove it when its subtree is fully processed, and test membership in that set instead of scanning ancestors:

```ts
type PathSet = Set<object>;

function walk(root: unknown, path: PathSet = new Set()): void {
  const pending: { value: unknown; isExit?: boolean }[] = [{ value: root }];
  for (let node = pending.pop(); node; node = pending.pop()) {
    if (node.isExit) { path.delete(node.value as object); continue; }
    const { value } = node;
    if (value === null || typeof value !== "object") continue;
    if (path.has(value)) continue; // cycle: let the caller/serializer surface it
    path.add(value);
    pending.push({ value, isExit: true }); // leave the path once children are done
    for (const child of Object.values(value)) pending.push({ value: child });
  }
}
```
Benchmark complexity-sensitive changes with a deep-but-acyclic fixture (e.g. a 20k+ level chain) under a tight time budget so a reintroduced quadratic scan fails CI instead of surfacing as a slow production hang.

3. When replacing a per-node/sequential algorithm with a batched or otherwise restructured one (e.g. BFS per hop across a whole frontier instead of per source node), explicitly verify whether result ordering, tie-breaking, and "which edge/record wins" semantics are preserved. If they are not — and especially if downstream consumers (APIs, tests, tools) depend on a specific order — call out the change explicitly in the PR/changelog rather than asserting equivalence; add a regression test pinning the new semantics.

4. Keep pre-scan/"does this need work" checks in lockstep with the main algorithm: reading all sibling fields eagerly during a decision pass (instead of lazily, stopping at the first positive result) can change how many times side-effecting accessors run and therefore what value the main pass later observes — re-pin behavioral tests deliberately when this changes, don't let it drift silently.