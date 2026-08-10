---
title: Consistent, Guarded Ranking
description: 'When implementing sorting/ranking or token-based relevance in retrieval
  pipelines, treat the algorithm as a system with strict contracts:


  1) Keep ranking features consistent across stages'
repository: mvanhorn/last30days-skill
label: Algorithms
language: Python
comments_count: 5
repository_stars: 57799
---

When implementing sorting/ranking or token-based relevance in retrieval pipelines, treat the algorithm as a system with strict contracts:

1) Keep ranking features consistent across stages
- If a value (e.g., relevance rank key) is computed for display, reuse the same computation (same text fields, same rounding/bucketing, same tie-break order) for upstream slot selection. Don’t recompute with different inputs like title-only vs title+body.

2) Guard token matching against over-grounding
- Head tokens and fallback matching must be “discriminating.” Avoid substring false positives (e.g., matching “code” inside “barcode”). Anchor fallback matching to word starts (prefix-anchored) or otherwise enforce word-boundary semantics appropriate to the tokenization.

3) Make heuristic gates parameter-correct and ordered
- Filters derived from request parameters (date windows, query heuristics, domain-sweep gating) must reflect the requested range and provider behavior. Order guards so broader heuristics (like “vs” logic or domain-word matches) can’t override question/length/window constraints.

4) Lock the behavior with regression tests
- Add tests for the specific false-positive/edge cases that drove the fixes (different text inputs, substring containment, historical window coverage, ambiguous heuristics).

Example: use a single source of truth for slot sort keys
```python
def slot_key(post: dict, prepared_query, relevance_fn, display_rank_fn) -> tuple:
    # Ensure relevance used here is computed from the same fields
    # that display_rank_fn uses.
    text = f"{post.get('title') or ''} {post.get('selftext') or ''}"  # same as display path
    rel = relevance_fn(prepared_query, text)

    # Tie-break structure must match display ordering.
    engagement = post.get("engagement") or {}
    has_comments = 1 if (engagement.get("num_comments") or 0) > 0 else 0
    rounded_rel = round(rel, 1)

    return (
        has_comments,
        rounded_rel,
        engagement.get("score") or 0,
        # optionally keep stable incoming order if equal
    )
```
Apply the same principle to entity grounding: only relax matching rules when you can prove they don’t introduce substring/general-token false positives.