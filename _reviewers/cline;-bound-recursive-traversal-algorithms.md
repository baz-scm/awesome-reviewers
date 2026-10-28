---
title: Bound recursive traversal algorithms
description: 'When an algorithm recursively or iteratively walks a self-referential
  or attacker-influenced structure (symlinks in an archive, git trees, nested directories),
  it must be proven to terminate and stay bounded, not just assumed to:'
repository: cline/cline;
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 70964
---

When an algorithm recursively or iteratively walks a self-referential or attacker-influenced structure (symlinks in an archive, git trees, nested directories), it must be proven to terminate and stay bounded, not just assumed to:

- Detect cycles/self-references explicitly (a symlink pointing at `.`, an ancestor, or a sibling that loops back) and skip them rather than re-expanding indefinitely.
- Cap both recursion depth and total work (e.g. `MAX_LINK_DEPTH`, `MAX_LINK_EXPANSIONS`) so a hostile or malformed input can't cause exponential blow-up or a hang; fail gracefully (e.g. add to a `skippedPaths` list) instead of crashing.
- Back any claim about an algorithm's behavior (e.g. "this merge can't fail because keys never collide", "read-tree without `-m` only fails on path collisions") with a reproducible test on realistic data, not just a comment — the discussion catches a reviewer's confident-but-wrong assumption that was only disproved by an actual repro.
- When a detection/matching algorithm trades off false positives against false negatives (e.g. a degenerate-output heuristic over a bounded tail window), state the tradeoff and the reasoning for the chosen bound explicitly near the threshold constant, so future readers don't "fix" it into a regression.

Example pattern for bounding a recursive expansion:
```ts
const MAX_LINK_DEPTH = 8;
const MAX_LINK_EXPANSIONS = 200; // caps total work for pathological link graphs

function addLinked(relativePath: string, repoPath: string, target: string, depth: number) {
  if (depth > MAX_LINK_DEPTH || expansions++ > MAX_LINK_EXPANSIONS || isAncestorOrSelf(resolved, repoPath)) {
    skippedPaths.push(repoPath);
    return;
  }
  // ...expand one level, recurse with depth + 1
}
```
Add a test that feeds the algorithm a deliberately cyclic/adversarial input and asserts it finishes quickly with only the expected real content processed.