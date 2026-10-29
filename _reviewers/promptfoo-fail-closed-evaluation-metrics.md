---
title: Fail-closed evaluation metrics
description: 'When implementing deterministic grading/scoring logic for model or agent
  outputs, design each rule to fail-closed on missing, ambiguous, or edge-case data
  rather than silently awarding a pass. Concretely:'
repository: promptfoo/promptfoo
label: AI
language: Python
comments_count: 8
repository_stars: 26565
---

When implementing deterministic grading/scoring logic for model or agent outputs, design each rule to fail-closed on missing, ambiguous, or edge-case data rather than silently awarding a pass. Concretely:

1. Treat missing or malformed annotations (e.g., an absent `ok` flag, missing `tool` identity) as low-confidence data that blocks a pass, rather than letting the rule default to success or get ignored. Low data quality should override an otherwise high aggregate score.
2. Explicitly reject degenerate inputs (empty traces, traces with no actions/verification at all) with a clear failing result instead of letting every inapplicable rule vacuously "pass" and average into a good score.
3. Verify signals by position and content quality, not just substring presence anywhere in the text — e.g., a closing/summary marker should only count if it appears in the final step with non-blank content, not if it appears mid-trace or as whitespace.
4. Make boundary/adjacency checks scan the correct window (e.g., "anywhere before the first action," "strictly between first and last action") instead of brittle immediate-adjacency checks that break when an unrelated step is inserted.
5. Normalize inputs consistently (e.g., case-insensitive term counting) and provide fallback identities for missing optional fields so metrics like retry-loop detection can't be defeated by omitting metadata.
6. Keep the documented description of each heuristic in sync with what it actually computes (e.g., call a repeated-term cap a "repeated-term cap," not a "drift detector") so reasoning strings and docs don't overstate the metric's guarantees.

Example of fail-closed aggregation:
```python
passed = score >= THRESHOLDS["pass_score"] and data_quality != "low"
```
Add regression tests for each edge case (missing fields, degenerate traces, boundary positions) to lock in the fail-closed behavior.