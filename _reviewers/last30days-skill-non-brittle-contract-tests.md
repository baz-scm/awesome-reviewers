---
title: Non-brittle Contract Tests
description: 'When writing tests, assert the real behavioral contract (the thing that
  could regress), not incidental formatting or brittle implementation details.


  Practical rules:'
repository: mvanhorn/last30days-skill
label: Testing
language: Python
comments_count: 6
repository_stars: 57799
---

When writing tests, assert the real behavioral contract (the thing that could regress), not incidental formatting or brittle implementation details.

Practical rules:
- Prefer contract/behavior checks that remain valid under real constraints (e.g., if output is truncated, assert required directives appear within the kept region and in the right envelope).
- Make harness-style tests deterministic and replay-only: freeze time, block real network calls, and use recorded fixtures.
- Avoid vacuous or misleading metrics: if the test expects structural outcomes (e.g., multi-member clusters), fail or score appropriately when the structure doesn’t form.
- Remove tautological assertions that cannot fail given earlier passing assertions.
- Avoid brittleness from ordering or cardinality: search by key (e.g., plugin name) instead of assuming single-entry lists or stable ordering.
- Avoid “security theatre”/non-functional checks that only verify text literals in config without meaningful behavioral coverage.

Example (truncation-survival contract):
```python
def kept_region(text: str) -> str:
    return text[: text.index("## Ranked Evidence Clusters")]

text = render.render_compact(sample_report())
head = kept_region(text)

assert "SYNTHESIS CONTRACT" in head
assert "<!-- END EVIDENCE FOR SYNTHESIS -->" not in head  # tail-only checks don’t help
```

Apply these principles so test failures pinpoint the true regression and don’t break due to incidental changes (ordering, redundant guards, or irrelevant text).