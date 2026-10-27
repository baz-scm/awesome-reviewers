---
title: Cache correctness invariants
description: When implementing or modifying caching used for analysis/validation,
  treat “what’s cached” and “when it’s updated” as invariants. Ensure (1) the cache
  captures *all relevant dependency/value forms* (not just a narrow subset like named
  identifiers) and (2) the cache is *populated in the correct order* so later reads
  see required derived values.
repository: facebook/react#b4
label: Caching
language: TypeScript
comments_count: 2
repository_stars: 251885
---

When implementing or modifying caching used for analysis/validation, treat “what’s cached” and “when it’s updated” as invariants. Ensure (1) the cache captures *all relevant dependency/value forms* (not just a narrow subset like named identifiers) and (2) the cache is *populated in the correct order* so later reads see required derived values.

Actionable checklist:
- Avoid cache source narrowing: if your logic filters inputs (e.g., only `Identifier`/named forms), expand it or explicitly document and test the missing cases.
- Add targeted fixtures/TODOs for suspected gaps: when a predicate like `isNamedIdentifier` might omit dependencies, lock the expectation with a test.
- Preserve cache population order: if derived metadata (e.g., phi derivations) is needed by later instruction traversal in successor/fallthrough blocks, record/update it before those reads.
- Be cautious with snapshots/loop structure: snapshot only when the subsequent phase expects a fully-populated cache; otherwise you can freeze incomplete state.

Example pattern to preserve:
```js
// Ensure phi-derived values are recorded before walking instructions
for (const block of fn.body.blocks.values()) {
  recordPhiDerivations(block, context); // populate derivations for later reads
}

for (const block of fallthroughBlocks) {
  for (const inst of block.instructions) {
    // reads here must see phi-derived entries previously recorded
    readFromDerivationCache(inst, context);
  }
}
```

If you need to change cache behavior, require a fixture that exercises the previously suspected edge case and validate that successor-block instruction walks observe the expected cached entries.