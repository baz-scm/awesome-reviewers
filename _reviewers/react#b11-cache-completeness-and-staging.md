---
title: Cache completeness and staging
description: 'Ensure derived-analysis caches are both *complete* and *staged correctly*.


  - **Don’t silently drop sources:** If cache population filters to a narrow subset
  of identifiers/sources (e.g., only “named identifiers”), either broaden it or explicitly
  document why the filtered cases are impossible. Add a **TODO + fixture** for tricky
  inputs so regressions are...'
repository: facebook/react#b11
label: Caching
language: TypeScript
comments_count: 2
repository_stars: 251894
---

Ensure derived-analysis caches are both *complete* and *staged correctly*.

- **Don’t silently drop sources:** If cache population filters to a narrow subset of identifiers/sources (e.g., only “named identifiers”), either broaden it or explicitly document why the filtered cases are impossible. Add a **TODO + fixture** for tricky inputs so regressions are caught.
- **Update cache before it’s read:** When traversing control-flow (basic blocks/PHIs), record/populate producer-derived cache entries (e.g., PHI derivations) **before** walking instructions in blocks that consume those values. If you change the order of operations, verify you still populate entries like `x@2` before they’re referenced.

Example (correct staging for PHIs):
```js
// Producer phase: record PHI-derived values into the cache for the block
recordPhiDerivations(phiBlock, context);

// Consumer phase: now walk the fallthrough block and read cached types/values
for (const instr of fallthroughBlock.instructions) {
  // should be able to find cached entries like x@2
  useValue(instr, context);
}
```

These practices prevent validation/analysis from operating on incomplete cached state and make changes to cache logic (source tracking, snapshots, pass ordering) robust.