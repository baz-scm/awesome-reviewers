---
title: Bounded, cycle-safe traversal
description: When an algorithm walks a structure that can revisit the same state —
  recursive symlinks, self-referential trees, paginated/indexed sets, or sequences
  with repeated values — explicitly define the invariant it must preserve (each real
  item processed once, no infinite recursion, the correct occurrence is matched) and
  enforce it in code rather than assuming...
repository: cline/cline#&&sleep 4
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 70980
---

When an algorithm walks a structure that can revisit the same state — recursive symlinks, self-referential trees, paginated/indexed sets, or sequences with repeated values — explicitly define the invariant it must preserve (each real item processed once, no infinite recursion, the correct occurrence is matched) and enforce it in code rather than assuming the input is well-behaved.

Concretely:
- Detect cycles/self-reference before recursing or expanding (e.g., a symlink whose target is `.`, `..`, or an ancestor/sibling already being copied must be skipped and reported, not re-expanded).
- Cap total work (expansion count, depth, result size) independently of cycle detection, since adversarial or merely unlucky inputs (many links fanning into one small target) can still blow up combinatorially even without a literal cycle.
- When state is maintained incrementally (cursors, offsets, run counts), re-derive or adjust the index after every mutation (skip, undo, insert) so it keeps pointing at the same logical item rather than drifting.
- Before "fixing" behavior you believe is broken in an underlying primitive (git plumbing, library call), write a minimal repro to confirm the actual behavior; don't patch around an assumed bug that a quick script would disprove.
- Validate the invariant with a test that targets the edge case directly, and where the state space is large (many action sequences, many link topologies), consider property-based/fuzz testing that asserts the invariant holds across randomized sequences rather than just the happy path.

Example from a skill installer that follows symlinks when copying a directory tree:
```ts
function addLinked(relativePath: string, repoPath: string, target: string, depth: number) {
  const resolved = normalizeRelativePath(posix.join(posix.dirname(repoPath), target));
  // Cap recursion depth and reject links back into an ancestor/already-copied dir.
  if (resolved === undefined || depth > MAX_LINK_DEPTH || isAncestorOrSelf(resolved, repoPath)) {
    skippedPaths.push(repoPath);
    return;
  }
  // ...expand `resolved`, counting against a global expansion cap...
}
```
This keeps traversal correct and terminating even when the input graph loops back on itself, and keeps incremental state (cursors, matched indices) consistent as the underlying collection changes.