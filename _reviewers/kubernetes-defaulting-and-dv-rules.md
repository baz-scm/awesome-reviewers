---
title: Defaulting and DV Rules
description: 'When evolving an API with new fields, treat defaulting/mirroring and
  declarative validation as a coupled compatibility problem.


  1) Mirror/default fields must preserve client intent'
repository: kUbernetes/kUbernetes
label: API
language: Go
comments_count: 5
repository_stars: 128688
---

When evolving an API with new fields, treat defaulting/mirroring and declarative validation as a coupled compatibility problem.

1) Mirror/default fields must preserve client intent
- If you introduce a new field that “mirrors” legacy fields via defaulting, explicitly document and test the patch/update behavior for skewed clients.
- Ensure old clients can still set legacy fields (e.g., `hostNetwork`) without being unintentionally overwritten by defaulting derived from new fields (e.g., `defaultNetwork`).
- If the only safe reconciliation requires both fields to agree, enforce this contract (via validation) and/or implement update strategies that either (a) assist only in well-defined legacy-to-new migrations or (b) fail with a clear error when the request is ambiguous.

2) Declarative validation migration: only remove manual checks when it’s truly equivalent
- If the DV mechanism can’t express the constraint due to API shape/nullability limitations, keep handwritten validation and add a comment explaining why it can’t be migrated yet.
- If DV tags are alpha/beta/still shadowed, keep manual validation as the authoritative behavior until the corresponding tags graduate to stable.
- Be careful with DV “shadowing” scope: DV tags on a field may cause validation to apply to parent fields/other constraints unexpectedly. Keep DV changes limited to the intended constraint.

Practical pattern
- Prefer “validation + explicit reconciliation” over implicit defaulting that overwrites other fields.
- Keep handwritten validation until DV is demonstrably equivalent in behavior (including error locations/messages you rely on).

Illustrative (constraint kept manual when DV can’t represent the mutual exclusion)
```go
// Exactly one of Value or ValueFrom must be specified.
// TODO: DV migration blocked by current API shape (non-nilable/union tag limitations).
func validateCounter(c *ConsumeCounter, fldPath *field.Path) field.ErrorList {
	allErrs := field.ErrorList{}
	if c.Value == (resource.Quantity{}) == (c.ValueFrom == nil) {
		allErrs = append(allErrs, field.Invalid(fldPath, c,
			"exactly one of value or valueFrom must be specified"))
	}
	return allErrs
}
```

Result: API additions remain patch-compatible across client versions, and constraints don’t silently change semantics during DV migration.