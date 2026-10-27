---
title: Use Consistent Public Names
description: Use established naming conventions and make names precise—especially
  for anything public (props, exported functions/types, options objects) or that implies
  semantics.
repository: facebook/react#b12
label: Naming Conventions
language: JavaScript
comments_count: 6
repository_stars: 251896
---

Use established naming conventions and make names precise—especially for anything public (props, exported functions/types, options objects) or that implies semantics.

Practical rules:
1) Prevent identifier typos and silent fallbacks
- If you rename an identifier, verify no legacy misspellings still exist.
- Avoid patterns where wrong names quietly hit defaults.

```js
// Before: typo risk
const env = props.expectedEnviromentName || 'Server';
// After: fix name, then grep for the old misspelling before merge
const env = props.expectedEnvironmentName || 'Server';
```

2) Normalize at the source, not via repeated adapters
- If a naming scheme requires translation (e.g., native `topPress` → React `press`), remove/avoid the special-case prefix so downstream doesn’t need to re-implement conversion logic.

3) Follow existing naming conventions for public “surface area”
- For option-like types, prefer the project’s established pattern (e.g., `${ucfirst(methodName)}Options`).
- Be cautious renaming types that appear in published/consumed declaration files; align with the existing convention rather than inventing new names.

4) Let names encode semantics (target vs limit; Promise vs Thenable)
- Choose names that match behavior: a “hint” is a target/approximation, while a “max” is a hard bound.
- Prefer the name that users most often expect when behavior matches that concept (e.g., “Promise” for thenables that act like promises), and ensure the displayed naming is consistent with reality.

5) Maintain compatibility with explicit aliases
- When moving away from an `unstable_` name (or similar), provide explicit exported aliases to avoid breaking consumers unnecessarily.