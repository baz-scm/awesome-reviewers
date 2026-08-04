---
title: No Silent Null Artifacts
description: When a workflow stage can legitimately have missing data, treat the missing
  artifact as an explicit, validated state—not as an absent file/implicit default.
repository: awslabs/aidlc-workflows
label: Null Handling
language: Markdown
comments_count: 2
repository_stars: 3849
---

When a workflow stage can legitimately have missing data, treat the missing artifact as an explicit, validated state—not as an absent file/implicit default.

Apply this in two ways:

1) Declare optional inputs explicitly (so tooling can’t miss the leak)
- If downstream logic can use something only when it exists (e.g., a decision pack), declare it as an **optional consume** in the consuming stage.
- Ensure upstream validation (e.g., coverage/guards) verifies the dependency is actually wired and referenced.

2) On any “skip/jump” path, still write the required record as an explicit empty fact
- If control flow skips a questionnaire step, you must still create the artifact that records “None/empty” rather than omitting it.
- This prevents downstream stages from treating “missing file” as “unknown,” which is effectively a null.

Minimal pattern
- Use optional consumes for legitimately absent artifacts.
- Use an “empty inventory”/placeholder record for required facts.

Example (stage metadata intent)
```yaml
# consuming stage
consumes:
  - artifact: decision-pack
    required: false   # optional, but explicitly declared
  - artifact: intent-statement
    required: true
```
```md
<!-- skip path: still create the artifact -->
# source-inventory.md
sources:
  - type: none
    note: "Recorded during skip-ahead; questionnaire did not run."
```

Outcome: downstream stages never rely on silent nulls (missing artifacts, non-written placeholders, or prose-only fallbacks) and null/unknown states are either explicitly represented or validated away.