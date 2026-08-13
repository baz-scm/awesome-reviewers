---
title: Deterministic Resolution With Confidence
description: 'When your system combines configurations or routes control flow, make
  the “resolution function” semantics explicit and safe: (1) define merge/override
  behavior precisely to prevent silent data loss, and (2) treat any heuristic inference
  from evidence as tentative—gate it with confidence and require explicit confirmation.'
repository: bmad-code-org/bmad-method
label: Algorithms
language: Markdown
comments_count: 3
repository_stars: 51859
---

When your system combines configurations or routes control flow, make the “resolution function” semantics explicit and safe: (1) define merge/override behavior precisely to prevent silent data loss, and (2) treat any heuristic inference from evidence as tentative—gate it with confidence and require explicit confirmation.

Apply this in three places:

1) Configuration/agent resolution (merge semantics)
- Write the exact structural rules: what overrides scalars, what deep-merges tables, how arrays merge (e.g., by keyed identity vs append), and what happens when files are missing.
- Avoid vague phrases like “later wins” unless your behavior is fully specified.

2) State-aware routing (control flow)
- Detect existing artifacts/state first (e.g., spec statuses) and route to the correct resume step.
- “Never skip steps” means don’t omit required stages; it does not prohibit resuming at the correct stage based on detected state.

3) Heuristic detection (data-driven inference)
- If you infer workflow/state from history/logs, treat it as a hint:
  - collect evidence,
  - compute confidence,
  - only suggest when confidence is above a threshold,
  - always ask the user to confirm or correct.

Example pattern (resolution + confidence-hinted detection):
```yaml
resolution_rules:
  scalars: "override"
  tables: "deep-merge"
  arrays:
    merge_by_key_when_identifiable: true   # e.g., code/id keyed arrays
    else: "append"

heuristic_detection:
  enabled: true
  confidence_threshold: 0.7
  indicators:
    gitflow:
      - pattern: "develop|release/*|hotfix/*"
        weight: 0.8
  output:
    show_evidence: true
  interaction:
    confirm_required: true
```

This prevents two common algorithmic failure modes: (a) “silent drops” from underspecified merge logic, and (b) “false certainty” from turning heuristics into irreversible decisions.