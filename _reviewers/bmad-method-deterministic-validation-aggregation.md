---
title: Deterministic Validation Aggregation
description: 'When implementing checklist/workflow validation, treat the process like
  a deterministic algorithm:


  - **Total coverage**: execute steps in order; evaluate **every** checklist item/section;
  never skip.'
repository: bmad-code-org/bmad-method
label: Algorithms
language: Xml
comments_count: 2
repository_stars: 51859
---

When implementing checklist/workflow validation, treat the process like a deterministic algorithm:

- **Total coverage**: execute steps in order; evaluate **every** checklist item/section; never skip.
- **Complete input reads**: don’t “sample”; if inputs are large, use **deterministic sequential chunk reads** and **record covered ranges** until the full content is processed.
- **Evidence-backed verdicts**: every verdict other than **N/A** must include concrete evidence from the target document. Use **N/A only** when an explicitly stated condition is truly not applicable—never to hide missing evidence.
- **Closed-set criticality classification**: determine “critical” checks **only** from an explicit closed set of markers (e.g., item tags/attributes like `critical="true|yes"`, or dedicated headings such as `CRITICAL`, `MUST FIX`, `MUST-FIX`, etc.). Do **not** infer criticality from generic keywords.
- **Deterministic final verdict**: compute the final status using a fixed rule from item verdicts—e.g.,

```pseudo
hasAnyFail = any(item.verdict == FAIL)
hasCriticalFailOrPartial = any(item.critical && (item.verdict == FAIL || item.verdict == PARTIAL))

if hasCriticalFailOrPartial or hasAnyFail:
  finalStatus = FAIL
else:
  finalStatus = PASS
```

Applying this standard prevents flaky/non-repeatable results and makes validation outcomes consistent, auditable, and safe to automate—especially when multiple checklist items interact.