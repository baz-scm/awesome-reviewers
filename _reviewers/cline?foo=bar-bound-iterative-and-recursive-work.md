---
title: Bound iterative and recursive work
description: 'When an algorithm scans, searches, or recursively traverses a space,
  make sure its work is bounded by the size of the actual problem rather than by brute
  force over every intermediate step. Two recurring failure modes to watch for:'
repository: cline/cline?foo=bar
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 71082
---

When an algorithm scans, searches, or recursively traverses a space, make sure its work is bounded by the size of the actual problem rather than by brute force over every intermediate step. Two recurring failure modes to watch for:

1. Brute-force scanning instead of skip-ahead. A minute-by-minute (or otherwise unit-by-unit) scan that could instead jump directly to the next candidate is a correctness smell as much as a performance one — e.g. a cron scheduler that walked every minute through `formatToParts` to find a yearly date (`0 0 29 2 *`) took seconds instead of ~1ms once it skipped whole days that couldn't match the calendar fields. Prefer computing the next viable candidate analytically and falling back to fine-grained stepping only near an actual match (to preserve edge cases like DST folds or date-line changes).

2. Unbounded recursion/expansion over self-referential or cyclic structures. Any traversal that can revisit the same node (symlinks pointing at `.`, `..`, or a sibling that loops back; graph traversal in general) must detect cycles/self-reference and cap total expansions (e.g. `MAX_LINK_DEPTH`, `MAX_LINK_EXPANSIONS`) so a malicious or accidental loop fails fast or degrades gracefully instead of hanging or blowing up exponentially.

When adding such an optimization or guard, verify it with deterministic tests that assert on the number of operations performed (e.g. capping `formatToParts` calls, or asserting a fixed number of expansions) rather than relying on wall-clock timing, which is flaky and doesn't prove the complexity bound holds.