---
title: Fail-Fast Validation Gates
description: 'When performing checklist-style validations (or any structured verification),
  implement error handling that is fail-fast, deterministic, and human-actionable:'
repository: bmad-code-org/bmad-method
label: Error Handling
language: Xml
comments_count: 3
repository_stars: 51859
---

When performing checklist-style validations (or any structured verification), implement error handling that is fail-fast, deterministic, and human-actionable:

- **Fail closed on “no applicable checks.”** If the validator computes `applicable_count == 0`, do **not** default to PASS. Emit an explicit **NEEDS_REVIEW** gate decision and warning so gaps don’t masquerade as success.
- **Align reporting/remediation to gate logic.** Ensure the remediation buckets match the computed gate/criticality:
  - **Must Fix** = critical **FAIL** + critical **PARTIAL**
  - **Should Improve** = non-critical **FAIL** + non-critical **PARTIAL**
- **Halt on internal incompleteness/inconsistency.** Add sanity checks that detect partial parsing or processing loss and **stop** rather than continue with incomplete results. Example: compare *parsed vs expected* item counts and **HALT** if divergence exceeds a threshold (e.g., `> 10%`).

Example (illustrative):
```pseudo
applicable_count = pass_count + partial_count + fail_count

if applicable_count == 0:
  gate = "NEEDS_REVIEW"  // fail-closed, not PASS
  warn("No applicable checklist items; validation cannot determine correctness")
else if critical_fail_count > 0 or critical_partial_count > 0 or fail_count > 0:
  gate = "FAIL"
else:
  gate = "PASS"

// Remediation alignment
must_fix = critical_fail_items + critical_partial_items
should_improve = noncritical_fail_items + noncritical_partial_items

// Parsing sanity check
if parsed_item_count diverges from expected_item_count by more than 10%:
  HALT("Checklist parsing incomplete; aborting validation")
```

Apply this standard to validation/verification systems so failures are detected early, success isn’t falsely granted, and outputs drive clear next actions.