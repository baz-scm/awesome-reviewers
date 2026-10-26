---
title: Algorithm invariants and ordering
description: 'When implementing complex allocation/selection algorithms, require three
  things in code review:


  1) **Explicit accounting invariants (no double-count / no negative “available”):**'
repository: kUbernetes/kUbernetes
label: Algorithms
language: Go
comments_count: 5
repository_stars: 128688
---

When implementing complex allocation/selection algorithms, require three things in code review:

1) **Explicit accounting invariants (no double-count / no negative “available”):**
   - Clearly separate “already-retained” vs “free-to-take” sets.
   - When computing distribution/remainder/balance, subtract retained impact exactly once, and never subtract retained amounts from a variable that was already initialized with the free-only view.
   - Add assertions/tests for edge cases where retained exceeds the computed distribution or where the remaining range collapses.

2) **Comparator/ordering correctness matches the priority model:**
   - Ordering decisions must compare the *intended* fields first (e.g., structural priority tier), not whatever happens to be at index 0.
   - If tie-breaking depends on multiple attributes, compute those attributes across the whole set (or in the correct order) rather than using a partial/positional surrogate.

3) **Deduplication when items span partitions:**
   - If sortable entities can appear in multiple topology regions (e.g., an UncoreCache spanning NUMA nodes), maintain a “seen/added” set so the final order doesn’t duplicate the same entity and distort counts.

Practical checklist for reviewers:
- Does the code define which sets represent retained vs allocatable, and is that consistent across all steps?
- Are there any places where the same quantity can be subtracted twice (or included twice) through reused variables/maps?
- Are loop bounds/range calculations correct when retained items dominate (e.g., `minNUMAs > maxNUMAs` cases)?
- Do comparator functions implement the priority tiering exactly as specified, and are there tests where the “best” element is not at index 0?
- For sorting across hierarchical partitions, are duplicates prevented when entities span multiple regions?

Example pattern to enforce invariant #3 (dedupe while sorting):
```go
added := cpuset.New()
for _, region := range regions {
  avail := availableSet.In(region)
  // If an entity can be present in multiple regions, remove already-added.
  avail = avail.Difference(added)
  // Now select from avail, then mark as added.
  result = append(result, avail.List()...)
  added = added.Union(avail)
}
```

If you adopt these rules consistently, most of the failure modes discussed (negative availability, skipped search due to wrong bounds, duplicated spanning items, and wrong “most important” ordering) become unlikely and are much easier to test and reason about.