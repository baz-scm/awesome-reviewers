---
title: Optimize With Correctness
description: When optimizing for performance, first determine whether the computation
  truly depends only on the requested subset or on document-wide/global evidence.
repository: firecrawl/pdf-inspector
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 13696
---

When optimizing for performance, first determine whether the computation truly depends only on the requested subset or on document-wide/global evidence.

Apply these rules:
1) Verify subset-vs-global dependencies: If a “filter” changes the inputs to global thresholding/evidence collection, you may break correctness (e.g., a one-page request being judged against the wrong floor).
2) Contain the tradeoff: If you must temporarily extract more than the requested scope for correctness, keep that behavior localized (small, auditable change) and document why the extra work exists and how to flip it.
3) Remove redundant static work/data: If large constant tables (metrics, lookup maps) are identical across variants, alias them to a single shared static, and enforce the behavior in generation tooling so duplicates don’t creep back.

Example patterns (mirroring the discussed approach):

- Localize “extract once with evidence” logic:
```rust
fn extract_with_evidence(doc: &Document, restore_order: bool) {
    let extract = |restore_order| {
        extract_pages_once(doc, /* ... */ restore_order)
    };

    // First pass gathers evidence using the needed scope.
    let (extraction, thresholds, _pages, _evidence) = extract(false)?;
    // Then apply the correction when verdict/thresholds are known.
    // (Keep any required widening of scope documented and easy to change.)

    Ok(())
}
```

- Deduplicate identical tables:
```rust
static COURIER: &[(char, u16)] = /* ... */;
// If metrics are identical across variants, alias instead of duplicating.
static COURIER_BOLD: &[(char, u16)] = COURIER;
```

Net effect: performance wins come from safe scope narrowing and memory deduplication, while correctness-critical global computations remain explicit, documented, and easy to audit/change.