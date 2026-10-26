---
title: Use stable, canonical names
description: When a name is part of an implicit contract (props/identifiers, exported
  symbols, consumer-facing types/options, or cross-layer event/data naming), follow
  a stable, canonical convention and avoid silent fallbacks.
repository: facebook/react#b1
label: Naming Conventions
language: JavaScript
comments_count: 6
repository_stars: 251878
---

When a name is part of an implicit contract (props/identifiers, exported symbols, consumer-facing types/options, or cross-layer event/data naming), follow a stable, canonical convention and avoid silent fallbacks.

Guidelines:
- Treat naming as correctness: if you rename a misspelled identifier, verify the old name is fully removed (don’t rely on defaults like `|| '...'` that can mask remaining usage).
- Centralize naming: prefer making the source emit canonical names and delete duplicated “name conversion” logic downstream.
- Preserve compatibility: for consumer-facing exports and semi-public type names, avoid breaking renames; follow existing conventions (e.g., `...Options`) and provide aliases for legacy identifiers.
- Keep semantics consistent: user-facing/debug naming should match the established meaning logic (don’t introduce ad-hoc labels).

Example (compatibility alias):
```js
// Prefer the canonical name
export {Activity} from './Activity';

// Keep the legacy/unstable export for compatibility
export {Activity as unstable_Activity} from './Activity';
```