---
title: Robust state-detection matching
description: When writing pattern-matching rules that classify dynamic content into
  discrete states (e.g., idle/working/blocked), design the matching logic to be correct,
  scoped, and non-overfit rather than tied to one observed snapshot.
repository: ogulcancelik/herdr#canary966c66ad
label: Algorithms
language: Toml
comments_count: 3
repository_stars: 46332
---

When writing pattern-matching rules that classify dynamic content into discrete states (e.g., idle/working/blocked), design the matching logic to be correct, scoped, and non-overfit rather than tied to one observed snapshot.

- Generalize patterns to cover all valid variations of a state, not just the single instance you happened to observe. For example, don't anchor on a specific selected option (`❯ 1. Yes`) if the selection can move (`❯ 2. No`); instead match the stable structural elements that persist across all variations (the question text plus the control footer).
- Bound the search region to where the signal is actually guaranteed to live. Prefer a narrow, bottom-anchored window (e.g., `bottom_non_empty_lines(N)`) over scanning the whole buffer (`whole_recent`) when the evidence shows the signal always appears near the bottom. Scanning too broadly risks matching stale or scrolled-past content as if it were current/live state.
- Add explicit exclusion conditions (`not = [...]`) when a lower-priority or fallback rule could otherwise match on residual/stale text that a more specific, higher-priority state should have overridden. This prevents fallback matches from clobbering a correct, more specific classification within the same scanned region.

Applying these principles keeps detection rules accurate across all real-world variations, avoids false positives from historical/stale data, and ensures correct priority resolution between overlapping patterns.