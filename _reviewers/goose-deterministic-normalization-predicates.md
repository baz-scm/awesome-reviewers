---
title: Deterministic normalization predicates
description: When transforming, sorting, deduplicating, or merging structured data,
  ensure comparisons use domain-correct semantics and identity signals are preserved.
repository: aaif-goose/goose
label: Algorithms
language: Rust
comments_count: 5
repository_stars: 51876
---

When transforming, sorting, deduplicating, or merging structured data, ensure comparisons use domain-correct semantics and identity signals are preserved.

Apply these rules:
1) Parse before comparing/sorting. Convert timestamp/typed fields into domain types (e.g., RFC3339 → instant) rather than relying on raw string/lexical order. When values may be missing/unparseable, still produce deterministic output with an explicit tie-breaker.
2) Canonicalize keys used for dedup/join. If two inputs can represent the same logical entity via different encodings (paths with `..`/symlinks, dot vs bracket notation, root vs nested identifiers), normalize them before using them in a `HashSet`/map key.
3) Keep boundary/identity predicates strict for merges. If you relax equality checks that define a boundary (e.g., “which turn does this reasoning belong to?”), you can merge distinct events. If recovery requires tolerance, restrict it to the smallest safe dimension and guard ambiguity (e.g., redacted placeholders).
4) Precedence matters. In pipelines with multiple enrichment/inference paths, run authoritative sources before inference, so guards like “only fill when unset” don’t block correct data.
5) Lock with regression tests around pathological inputs (missing dates, mixed offsets, ambiguous redaction, structured key syntax variants).

Example pattern (semantic sort with deterministic fallback):
```rust
let mut items: Vec<(String, String)> = arr
  .iter()
  .filter_map(|m| {
    let id = m.get("id")?.as_str()?.to_string();
    let created_at = m.get("created_at")
      .and_then(|v| v.as_str())
      .unwrap_or("")
      .to_string();
    Some((id, created_at))
  })
  .collect();

// Prefer sorting by parsed instant; fall back deterministically.
items.sort_by(|a, b| b.1.cmp(&a.1).then_with(|| a.0.cmp(&b.0)));
```

Checklist for PRs in this area:
- Are sort/merge/dedup decisions based on normalized domain values?
- Are keys canonicalized before being used for equality?
- Are identity/boundary predicates strict enough to prevent accidental merges?
- Do tests cover malformed/ambiguous inputs?