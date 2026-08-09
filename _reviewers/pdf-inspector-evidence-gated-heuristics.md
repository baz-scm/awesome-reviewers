---
title: Evidence-Gated Heuristics
description: 'When implementing content extraction/layout algorithms, treat “heuristics”
  as *probabilistic classifiers*: constrain them with invariants, gate them with evidence,
  and lock behavior with targeted regression tests.'
repository: firecrawl/pdf-inspector
label: Algorithms
language: Rust
comments_count: 13
repository_stars: 13696
---

When implementing content extraction/layout algorithms, treat “heuristics” as *probabilistic classifiers*: constrain them with invariants, gate them with evidence, and lock behavior with targeted regression tests.

Practical standard (apply per heuristic):
1) State the invariant explicitly and enforce its shape
- Example invariants from the discussions: “marker must be line-start shaped”, “drop-cap target must be on the same page”, “a continuation must share the right geometry but also START a paragraph”.

2) Only compare like with like (units/scopes)
- Ensure coordinate/geometry comparisons use comparable quantities (e.g., line-step/leading rather than unrelated em-scaled fractions) and correct scope (don’t let previous-page coordinates influence current-page decisions).

3) Evidence-gate before acting
- Prefer multi-signal requirements: floors (min counts), sparsity (blank-on-some-rows), and contextual repetition across pages instead of single-instance acceptance.

4) Make classification value-driven, not structure-driven
- Don’t let headers/labels be the classifier; decide from observed values (e.g., marker columns identified via sparse marker values, not header text).

5) Add a failing boundary regression test for each “veto”
- For every guard you add (sentence-ending logic, hyphenation continuation exclusion, line-start marker shape, evidence thresholds), add a small test that would have corrupted output before the fix.
- Use synthetic fixtures for ordering/producer-format issues so byte order/layout is controllable.

Illustrative pattern (Rust-style):
```rust
fn maybe_merge_with_evidence(items: &[Item], context: &Ctx) -> Option<Merged> {
    // 1) Invariant + shape constraints
    if !context.invariant_holds(items) {
        return None;
    }

    // 2) Evidence gating (floors + sparsity / repeated-context)
    let evidence = context.evidence_score(items);
    if evidence < context.EVIDENCE_FLOOR {
        return None;
    }

    // 3) Finally apply transformation
    Some(context.apply_merge(items))
}
```

Outcome: fewer false positives (corruption) and fewer over-broad fixes, because heuristics only activate when their evidence is strong *and* their inputs match the invariant assumptions.