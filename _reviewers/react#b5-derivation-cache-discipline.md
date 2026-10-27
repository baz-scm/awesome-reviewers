---
title: Derivation Cache Discipline
description: When maintaining a derivation/analysis cache, ensure it is (a) complete
  about what it records and (b) populated in a dependency-safe order so later reads
  never rely on missing facts.
repository: facebook/react#b5
label: Caching
language: TypeScript
comments_count: 2
repository_stars: 251886
---

When maintaining a derivation/analysis cache, ensure it is (a) complete about what it records and (b) populated in a dependency-safe order so later reads never rely on missing facts.

Apply this standard:
1) Avoid overly narrow cache inputs. If your derivation cache only records certain identifier forms (e.g., “named identifiers only”), expand the source-extraction logic so all relevant value origins are captured.
2) Add targeted fixtures/TODOs for excluded paths. If there’s a prior check that could miss cases, create a regression test that demonstrates the previously-missed dependency.
3) Write-before-read in control-flow walks. For SSA/phi-style dependencies, record phi derivations (or equivalent “producer” facts) before traversing instructions/blocks that consume those derived values. If you introduce snapshots or change loop/pass ordering, re-verify that dependent reads occur after the corresponding cache writes.

Illustrative pattern:
```js
// Good: populate producer facts (phis) before consumer traversal
for (const block of fn.body.blocks.values()) {
  recordPhiDerivations(block, context); // write facts used by this block
}
for (const block of fn.body.blocks.values()) {
  for (const inst of block.instructions) {
    // read from cache; should now be present
    useTypeOfValue(context, inst);
  }
}
```
If you change ordering during debugging, immediately re-validate that the cache is still dependency-complete and that snapshots/iterations don’t reintroduce stale or missing entries.